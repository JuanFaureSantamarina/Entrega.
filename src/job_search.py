"""
Búsqueda automática de ofertas laborales.

Junta ofertas de varias fuentes (LinkedIn público, Remotive, Himalayas,
portales Workday / Greenhouse / Lever de empresas grandes), descarta las que
no encajan, les pone un puntaje según el perfil y guarda el resultado en
data/jobs/ofertas.json.

Cada fuente falla por separado: si una se cae, las demás siguen y el error
queda registrado en data/jobs/estado.json.
"""

import hashlib
import html
import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml


CONFIG_PATH = Path("config/search.yaml")
JOBS_DIR    = Path("data/jobs")
OFERTAS     = JOBS_DIR / "ofertas.json"
ESTADO      = JOBS_DIR / "estado.json"
DIAS_HISTORIAL = 45

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

UBICACIONES_REMOTAS_OK = (
    "worldwide", "anywhere", "latam", "latin america", "south america",
    "americas", "argentina", "global",
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def _norm(text: str) -> str:
    """Minúsculas y sin tildes, para comparar palabras clave."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return f" {text.lower()} "


def _contiene(frase: str, texto: str) -> bool:
    """La frase aparece al inicio de una palabra del texto (sirve para raíces como 'automatiza')."""
    frase = _norm(frase).strip()
    return bool(frase) and re.search(r"(?<!\w)" + re.escape(frase), texto) is not None


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html.unescape(text or ""))
    return re.sub(r"\s+", " ", text).strip()


def _http(url: str, data: dict | None = None, timeout: int = 30) -> str:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json, text/html"}
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _job_id(fuente: str, key: str) -> str:
    return f"{fuente}-" + hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def _oferta(fuente, key, empresa, puesto, link, ubicacion="", modalidad="",
            descripcion="", publicada="") -> dict:
    return {
        "id": _job_id(fuente, key),
        "fuente": fuente,
        "empresa": (empresa or "").strip(),
        "puesto": (puesto or "").strip(),
        "link": link,
        "ubicacion": (ubicacion or "").strip(),
        "modalidad": modalidad,
        "descripcion": _strip_html(descripcion)[:1500],
        "publicada": publicada,
    }


def _detectar_modalidad(*textos: str) -> str:
    t = _norm(" ".join(textos))
    if any(k in t for k in ("hibrid", "hybrid")):
        return "hibrido"
    if any(k in t for k in ("remot", "home office", "teletrabajo", "work from home")):
        return "remoto"
    if any(k in t for k in ("presencial", "on-site", "onsite", "on site")):
        return "presencial"
    return ""


# ─── Fuentes ──────────────────────────────────────────────────────────────────

def fetch_linkedin(cfg: dict, keywords: list[str]) -> list[dict]:
    """Búsqueda pública de LinkedIn (la que se ve sin iniciar sesión)."""
    src = cfg["fuentes"]["linkedin"]
    segundos = int(src.get("horas", 24)) * 3600
    ofertas = []
    # f_WT: 2 = remoto, 3 = híbrido
    for modo, modalidad in (("2", "remoto"), ("3", "hibrido")):
        for kw in keywords:
            for page in range(int(src.get("paginas_por_keyword", 1))):
                params = urllib.parse.urlencode({
                    "keywords": kw,
                    "location": src.get("ubicacion", "Argentina"),
                    "f_WT": modo,
                    "f_TPR": f"r{segundos}",
                    "start": page * 25,
                })
                url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{params}"
                try:
                    page_html = _http(url)
                except urllib.error.HTTPError as e:
                    if e.code in (400, 404):
                        break
                    raise
                cards = page_html.split("<li")
                for card in cards:
                    link = re.search(r'class="base-card__full-link[^"]*"\s+href="([^"?]+)', card)
                    title = re.search(r'base-search-card__title[^>]*>\s*([^<]+)', card)
                    if not link or not title:
                        continue
                    company = re.search(r'base-search-card__subtitle[^>]*>\s*(?:<a[^>]*>)?\s*([^<]+)', card)
                    loc = re.search(r'job-search-card__location[^>]*>\s*([^<]+)', card)
                    date = re.search(r'datetime="([^"]+)"', card)
                    href = html.unescape(link.group(1))
                    ofertas.append(_oferta(
                        "linkedin", href.rstrip("/").split("-")[-1] or href,
                        html.unescape(company.group(1)) if company else "",
                        html.unescape(title.group(1)),
                        href,
                        ubicacion=html.unescape(loc.group(1)) if loc else "",
                        modalidad=modalidad,
                        publicada=date.group(1) if date else "",
                    ))
                time.sleep(1.5)
    return ofertas


def fetch_remotive(cfg: dict, keywords: list[str]) -> list[dict]:
    ofertas = []
    for kw in keywords:
        url = "https://remotive.com/api/remote-jobs?" + urllib.parse.urlencode({"search": kw})
        data = json.loads(_http(url))
        for j in data.get("jobs", []):
            loc = j.get("candidate_required_location", "")
            if not any(u in _norm(loc) for u in UBICACIONES_REMOTAS_OK):
                continue
            ofertas.append(_oferta(
                "remotive", str(j.get("id")), j.get("company_name"), j.get("title"),
                j.get("url"), ubicacion=loc, modalidad="remoto",
                descripcion=j.get("description", ""), publicada=j.get("publication_date", ""),
            ))
        time.sleep(1)
    return ofertas


def fetch_himalayas(cfg: dict, keywords: list[str]) -> list[dict]:
    ofertas = []
    for offset in range(0, 400, 100):
        url = f"https://himalayas.app/jobs/api?limit=100&offset={offset}"
        data = json.loads(_http(url))
        jobs = data.get("jobs", [])
        if not jobs:
            break
        for j in jobs:
            paises = j.get("locationRestrictions") or []
            if paises and not any(u in _norm(" ".join(map(str, paises))) for u in UBICACIONES_REMOTAS_OK):
                continue
            link = j.get("applicationLink") or j.get("guid") or ""
            ofertas.append(_oferta(
                "himalayas", j.get("guid") or link, j.get("companyName"), j.get("title"),
                link, ubicacion=", ".join(map(str, paises)) or "Worldwide", modalidad="remoto",
                descripcion=j.get("description") or j.get("excerpt", ""),
                publicada=str(j.get("pubDate", "")),
            ))
        time.sleep(1)
    return ofertas


def fetch_workday(empresa: str, url: str) -> list[dict]:
    """Portales Workday: https://<tenant>.wdN.myworkdayjobs.com/<site>"""
    parsed = urllib.parse.urlparse(url)
    tenant = parsed.netloc.split(".")[0]
    site = [p for p in parsed.path.split("/") if p and not re.fullmatch(r"[a-z]{2}-[A-Z]{2}", p)][0]
    api = f"https://{parsed.netloc}/wday/cxs/{tenant}/{site}/jobs"
    ofertas = []
    for offset in (0, 20, 40):
        data = json.loads(_http(api, {"appliedFacets": {}, "limit": 20, "offset": offset,
                                      "searchText": "Argentina"}))
        posts = data.get("jobPostings", [])
        for p in posts:
            loc = p.get("locationsText", "")
            if "argentin" not in _norm(loc) and "buenos aires" not in _norm(loc) and "location" not in _norm(loc):
                continue
            path = p.get("externalPath", "")
            ofertas.append(_oferta(
                "workday", f"{tenant}{path}", empresa, p.get("title"),
                f"https://{parsed.netloc}/{site}{path}", ubicacion=loc,
                modalidad=_detectar_modalidad(p.get("remoteType", ""), p.get("title", "")),
                publicada=p.get("postedOn", ""),
            ))
        if len(posts) < 20:
            break
    return ofertas


def fetch_eightfold(empresa: str, hosts: list[str], domain: str, consultas: list[str],
                    ubicacion: str = "Argentina", max_por_consulta: int = 50) -> list[dict]:
    """Portales Eightfold (por ejemplo Mercado Libre). Prueba cada host hasta que uno responda."""
    ultimo_error = None
    for host in hosts:
        try:
            ofertas = []
            for q in consultas:
                for start in range(0, max_por_consulta, 10):
                    params = urllib.parse.urlencode({
                        "domain": domain, "query": q, "location": ubicacion,
                        "start": start, "num": 10, "sort_by": "timestamp",
                    })
                    data = json.loads(_http(f"https://{host}/api/apply/v2/jobs?{params}"))
                    posiciones = data.get("positions", [])
                    for p in posiciones:
                        locs = p.get("locations") or [p.get("location", "")]
                        loc = ", ".join(str(l) for l in locs if l)
                        if "argentin" not in _norm(loc) and "buenos aires" not in _norm(loc):
                            continue
                        modo = _norm(p.get("work_location_option", ""))
                        modalidad = ("hibrido" if "hybrid" in modo else "remoto" if "remote" in modo
                                     else "presencial" if "onsite" in modo or "on_site" in modo
                                     else _detectar_modalidad(p.get("name", "")))
                        link = p.get("canonicalPositionUrl") or f"https://{host}/careers?pid={p.get('id')}&domain={domain}"
                        ts = p.get("t_create") or p.get("t_update")
                        ofertas.append(_oferta(
                            "eightfold", f"{domain}-{p.get('id')}", empresa, p.get("name"), link,
                            ubicacion=loc, modalidad=modalidad,
                            descripcion=p.get("job_description", ""),
                            publicada=datetime.fromtimestamp(ts, timezone.utc).date().isoformat() if ts else "",
                        ))
                    if len(posiciones) < 10:
                        break
                    time.sleep(0.5)
            return ofertas
        except Exception as e:  # probar el siguiente host
            ultimo_error = e
    raise ultimo_error or RuntimeError("sin hosts configurados")


def fetch_greenhouse(slug: str) -> list[dict]:
    data = json.loads(_http(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"))
    ofertas = []
    for j in data.get("jobs", []):
        loc = (j.get("location") or {}).get("name", "")
        if "argentin" not in _norm(loc) and "buenos aires" not in _norm(loc) and "latam" not in _norm(loc):
            continue
        content = j.get("content", "")
        ofertas.append(_oferta(
            "greenhouse", str(j.get("id")), slug, j.get("title"), j.get("absolute_url"),
            ubicacion=loc, modalidad=_detectar_modalidad(loc, j.get("title", ""), content[:2000]),
            descripcion=content, publicada=j.get("updated_at", ""),
        ))
    return ofertas


def fetch_lever(slug: str) -> list[dict]:
    data = json.loads(_http(f"https://api.lever.co/v0/postings/{slug}?mode=json"))
    ofertas = []
    for j in data:
        cats = j.get("categories") or {}
        loc = cats.get("location", "") or ", ".join(cats.get("allLocations") or [])
        if "argentin" not in _norm(loc) and "buenos aires" not in _norm(loc) and "latam" not in _norm(loc):
            continue
        workplace = {"remote": "remoto", "hybrid": "hibrido", "onsite": "presencial"}.get(
            j.get("workplaceType", ""), "")
        ofertas.append(_oferta(
            "lever", j.get("id", ""), slug, j.get("text"), j.get("hostedUrl"),
            ubicacion=loc, modalidad=workplace or _detectar_modalidad(loc, j.get("text", "")),
            descripcion=j.get("descriptionPlain", ""),
            publicada=datetime.fromtimestamp(j.get("createdAt", 0) / 1000, timezone.utc).isoformat()
            if j.get("createdAt") else "",
        ))
    return ofertas


# ─── Filtro y puntaje ─────────────────────────────────────────────────────────

def puntuar(oferta: dict, cfg: dict) -> tuple[int, list[str]]:
    """Devuelve (puntaje 0-100, motivos). Puntaje -1 = descartada."""
    titulo = _norm(oferta["puesto"])
    texto = _norm(f"{oferta['puesto']} {oferta['descripcion']}")
    empresa = _norm(oferta["empresa"])
    motivos = []

    if any(_contiene(x, titulo) for x in cfg.get("excluir_titulos", [])):
        return -1, ["título excluido"]
    if oferta["modalidad"] == "presencial":
        return -1, ["presencial"]

    score = 0
    keywords = cfg["keywords"]["es"] + cfg["keywords"]["en"]
    match_titulo = [k for k in keywords if _contiene(k, titulo)]
    if match_titulo:
        score += 40
        motivos.append(f"título: {match_titulo[0]}")
    else:
        palabras = {"proceso", "process", "operacion", "operation", "administra", "admin",
                    "compras", "procurement", "finanz", "finance", "cobranza", "pagos",
                    "tesoreria", "costos", "contab", "accounting", "analista", "analyst",
                    "pasant", "intern", "trainee"}
        hits = [p for p in palabras if p in titulo]
        if not hits:
            return -1, ["título fuera de perfil"]
        score += 10 * min(len(hits), 2)
        motivos.append("título relacionado")

    skills = [s for s in cfg.get("skills_cv", []) if _contiene(s, texto)]
    if skills:
        score += min(len(skills) * 4, 25)
        motivos.append("skills: " + ", ".join(skills[:4]))

    if any(_contiene(e, empresa) for e in cfg.get("empresas_objetivo", [])):
        score += 15
        motivos.append("empresa objetivo")

    if oferta["modalidad"] in ("remoto", "hibrido"):
        score += 10
    else:
        motivos.append("modalidad a confirmar")

    if any(_contiene(s, titulo) for s in cfg.get("seniority_alta", [])):
        score -= 15
        motivos.append("seniority alta")
    if any(_contiene(k, titulo) for k in ("pasant", "intern", "trainee", "junior", "jr", "jovenes profesionales")):
        score += 5

    return max(0, min(100, score)), motivos


def _nicho(oferta: dict) -> str:
    t = _norm(f"{oferta['puesto']} {oferta['descripcion'][:500]}")
    admin = ("administra", "cobranza", "pagos", "payable", "receivable", "tesoreria", "treasury",
             "compras", "procurement", "costos", "contab", "accounting", "finance", "finanz")
    return "administracion" if any(a in t for a in admin) else "operaciones"


# ─── Orquestación ─────────────────────────────────────────────────────────────

def _cargar_existentes() -> dict:
    if not OFERTAS.exists():
        return {}
    return {o["id"]: o for o in json.loads(OFERTAS.read_text(encoding="utf-8"))}


def buscar(dry_run: bool = False, log=print) -> dict:
    cfg = load_config()
    fuentes_cfg = cfg["fuentes"]
    kw_es, kw_en = cfg["keywords"]["es"], cfg["keywords"]["en"]

    tareas = []
    if fuentes_cfg.get("linkedin", {}).get("activo"):
        tareas.append(("linkedin", lambda: fetch_linkedin(cfg, kw_es + kw_en)))
    if fuentes_cfg.get("remotive", {}).get("activo"):
        tareas.append(("remotive", lambda: fetch_remotive(cfg, kw_en)))
    if fuentes_cfg.get("himalayas", {}).get("activo"):
        tareas.append(("himalayas", lambda: fetch_himalayas(cfg, kw_en)))
    for w in fuentes_cfg.get("workday", []) or []:
        tareas.append((f"workday:{w['empresa']}", lambda w=w: fetch_workday(w["empresa"], w["url"])))
    for ef in fuentes_cfg.get("eightfold", []) or []:
        tareas.append((f"eightfold:{ef['empresa']}", lambda ef=ef: fetch_eightfold(
            ef["empresa"], ef["hosts"], ef["domain"], ef["consultas"],
            ef.get("ubicacion", "Argentina"), int(ef.get("max_por_consulta", 50)))))
    for slug in fuentes_cfg.get("greenhouse", []) or []:
        tareas.append((f"greenhouse:{slug}", lambda s=slug: fetch_greenhouse(s)))
    for slug in fuentes_cfg.get("lever", []) or []:
        tareas.append((f"lever:{slug}", lambda s=slug: fetch_lever(s)))

    estado = {"fecha": datetime.now(timezone.utc).isoformat(timespec="seconds"), "fuentes": {}}
    crudas = []
    for nombre, fn in tareas:
        try:
            res = fn()
            crudas.extend(res)
            estado["fuentes"][nombre] = {"ok": True, "encontradas": len(res)}
            log(f"  ✓ {nombre}: {len(res)} ofertas")
        except Exception as e:  # una fuente caída no frena al resto
            estado["fuentes"][nombre] = {"ok": False, "error": f"{type(e).__name__}: {e}"[:300]}
            log(f"  ✗ {nombre}: {type(e).__name__}: {e}")

    existentes = _cargar_existentes()
    hoy = datetime.now(timezone.utc).date().isoformat()
    nuevas, vistas = [], set()
    min_score = int(cfg.get("puntaje_minimo", 30))
    for o in crudas:
        if o["id"] in vistas or not o["link"] or not o["puesto"]:
            continue
        vistas.add(o["id"])
        score, motivos = puntuar(o, cfg)
        if score < min_score:
            continue
        o.update({"puntaje": score, "motivos": motivos, "nicho": _nicho(o),
                  "mercado": "exterior" if o["fuente"] in ("remotive", "himalayas") else "argentina"})
        if o["id"] in existentes:
            existentes[o["id"]].update({k: o[k] for k in ("puntaje", "motivos", "modalidad")})
            continue
        o["fecha_encontrada"] = hoy
        existentes[o["id"]] = o
        nuevas.append(o)

    limite = (datetime.now(timezone.utc) - timedelta(days=DIAS_HISTORIAL)).date().isoformat()
    todas = sorted(
        (o for o in existentes.values() if o.get("fecha_encontrada", hoy) >= limite),
        key=lambda o: (o.get("fecha_encontrada", ""), o.get("puntaje", 0)), reverse=True,
    )
    estado.update({"crudas": len(crudas), "nuevas": len(nuevas), "total": len(todas)})

    if not dry_run:
        JOBS_DIR.mkdir(parents=True, exist_ok=True)
        OFERTAS.write_text(json.dumps(todas, ensure_ascii=False, indent=1), encoding="utf-8")
        ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding="utf-8")

    return {"estado": estado, "nuevas": nuevas, "todas": todas}


def listar(min_score: int = 0, dias: int = 7) -> list[dict]:
    desde = (datetime.now(timezone.utc) - timedelta(days=dias)).date().isoformat()
    return [o for o in _cargar_existentes().values()
            if o.get("puntaje", 0) >= min_score and o.get("fecha_encontrada", "") >= desde]
