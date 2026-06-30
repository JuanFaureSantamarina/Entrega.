#!/usr/bin/env python3
"""
Job Application Automation CLI
Automatizá tus postulaciones laborales con IA (Claude).

Uso rápido:
  python main.py init
  python main.py apply --company "Empresa" --position "Desarrollador" --cover-letter
  python main.py niches list
  python main.py cv list
  python main.py cover-letter list
  python main.py track list
"""

import argparse
import os
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path


# ─── Terminal colors ──────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
CYAN   = "\033[36m"
RED    = "\033[31m"
DIM    = "\033[2m"


def c(color: str, text: str) -> str:
    return f"{color}{text}{RESET}"

def ok(msg):   print(c(GREEN,  f"✓ {msg}"))
def warn(msg): print(c(YELLOW, f"! {msg}"))
def err(msg):  print(c(RED,    f"✗ {msg}"), file=sys.stderr)
def info(msg): print(c(DIM,    f"  {msg}"))
def head(msg): print(f"\n{c(BOLD+BLUE, msg)}")


def load_env():
    env_path = Path(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_base_cv() -> dict:
    path = Path("data/base_cv.yaml")
    if not path.exists():
        err("No se encontró data/base_cv.yaml. Completá tu CV base primero.")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def make_slug(company: str, position: str) -> str:
    text = f"{company}_{position}"
    text = re.sub(r"[^\w\s-]", "", text).strip()
    text = re.sub(r"[\s]+", "_", text)
    return text[:60]


# ─── Command: init ────────────────────────────────────────────────────────────

def cmd_init(args):
    head("Verificando configuración...")

    if Path(".env").exists():
        ok(".env encontrado")
    else:
        warn("No hay .env — copiá .env.example a .env y completá tus credenciales")

    if os.environ.get("ANTHROPIC_API_KEY"):
        ok("ANTHROPIC_API_KEY configurada (para tailoring con IA)")
    else:
        warn("ANTHROPIC_API_KEY no configurada — podés usar CVs y cartas pre-armados igual")

    cv_path = Path("data/base_cv.yaml")
    if cv_path.exists():
        base_cv = yaml.safe_load(cv_path.read_text())
        name = base_cv.get("personal", {}).get("name", "")
        if name and name != "Tu Nombre Completo":
            ok(f"CV base: {name}")
        else:
            warn("CV base existe pero no fue completado — editá data/base_cv.yaml")
    else:
        err("No se encontró data/base_cv.yaml")

    from src.niche_manager import list_niches
    from src.templates_manager import list_niche_cvs, list_cover_letters
    niches      = list_niches()
    niche_cvs   = list_niche_cvs()
    cover_ltrs  = list_cover_letters()

    ok(f"{len(niches)} nichos: {', '.join(n['id'] for n in niches)}")

    if niche_cvs:
        ok(f"CVs por nicho: {', '.join(niche_cvs)}")
    else:
        warn("No hay CVs por nicho todavía — creá uno con: python main.py cv init-niche tech")

    if cover_ltrs:
        ok(f"Cartas de presentación: {', '.join(cover_ltrs)}")
    else:
        warn("No hay cartas de presentación — creá una con: python main.py cover-letter init")

    for d in ["output/cvs", "output/cover_letters"]:
        Path(d).mkdir(parents=True, exist_ok=True)
    ok("Carpetas de output listas")

    print()
    print(c(BOLD+CYAN, "Flujo recomendado:"))
    print(f"  1. Completá data/base_cv.yaml con tu info")
    print(f"  2. python main.py cv init-niche tech        (creá un CV por nicho)")
    print(f"  3. Editá data/cvs/tech.yaml para ese nicho")
    print(f"  4. Editá data/cover_letters/tech.txt")
    print(f"  5. python main.py apply -c 'Empresa' -p 'Puesto' --cover-letter")


# ─── Command: niches ──────────────────────────────────────────────────────────

def cmd_niches_list(args):
    from src.niche_manager import list_niches
    from src.templates_manager import list_niche_cvs, list_cover_letters

    niches    = list_niches()
    have_cvs  = set(list_niche_cvs())
    have_cls  = set(list_cover_letters())

    if not niches:
        warn("No hay nichos en config/niches/")
        return

    head("Nichos disponibles")
    w = max(len(n["id"]) for n in niches) + 2
    print(f"  {'ID':<{w}} {'Nombre':<24} {'CV':<5} {'Carta':<7} Descripción")
    print(f"  {'-'*w} {'-'*24} {'-'*5} {'-'*7} {'-'*28}")
    for n in niches:
        cv_mark = c(GREEN, "  ✓") if n["id"] in have_cvs else c(DIM, "  –")
        cl_mark = c(GREEN, "  ✓") if n["id"] in have_cls else c(DIM, "  –")
        print(f"  {c(CYAN, n['id']):<{w+9}} {n['name']:<24} {cv_mark}    {cl_mark}    {n.get('description','')}")


def cmd_niches_show(args):
    from src.niche_manager import load_niche
    try:
        niche = load_niche(args.niche_id)
    except ValueError as e:
        err(str(e)); sys.exit(1)
    head(f"Nicho: {args.niche_id}")
    print(f"  {c(BOLD,'Nombre:')}      {niche['name']}")
    print(f"  {c(BOLD,'Tono:')}        {niche.get('tone','-')}")
    print(f"  {c(BOLD,'Énfasis:')}     {niche.get('emphasis','-')}")
    print(f"  {c(BOLD,'Keywords:')}    {', '.join(niche.get('keywords',[]))}")


# ─── Command: cv ──────────────────────────────────────────────────────────────

def cmd_cv_list(args):
    from src.niche_manager import list_niches
    from src.templates_manager import list_niche_cvs

    have   = set(list_niche_cvs())
    niches = {n["id"]: n["name"] for n in list_niches()}

    head("CVs por nicho")
    all_ids = sorted(set(list(have) + list(niches.keys())))
    for nid in all_ids:
        name = niches.get(nid, nid)
        if nid in have:
            print(f"  {c(GREEN,'✓')} {c(CYAN, nid):<18} {name}  {c(DIM,'→ data/cvs/'+nid+'.yaml')}")
        else:
            print(f"  {c(DIM,'–')} {c(DIM, nid):<18} {c(DIM, name)}  (no creado)")

    print(f"\n  {c(DIM, 'Creá uno con: python main.py cv init-niche <niche_id>')}")


def cmd_cv_init_niche(args):
    from src.templates_manager import create_niche_cv, niche_cv_exists

    if niche_cv_exists(args.niche_id) and not args.force:
        warn(f"Ya existe data/cvs/{args.niche_id}.yaml — usá --force para sobreescribir")
        return

    path = create_niche_cv(args.niche_id)
    ok(f"CV creado en {path}")
    print(f"\n  {c(BOLD, 'Siguiente paso:')} editá {c(CYAN, str(path))} para adaptarlo al nicho '{args.niche_id}'")
    print(f"  Ajustá el summary, reordenando logros y skills relevantes para ese nicho.")


def cmd_cv_preview(args):
    from src.templates_manager import load_niche_cv, niche_cv_exists

    if args.niche and niche_cv_exists(args.niche):
        cv_data = load_niche_cv(args.niche)
        info(f"Usando CV del nicho '{args.niche}'")
    else:
        cv_data = load_base_cv()
        if args.niche:
            warn(f"No hay CV para el nicho '{args.niche}', usando CV base")

    ts   = datetime.now().strftime("%Y%m%d_%H%M")
    label = args.niche or "base"
    path  = Path("output/cvs") / f"CV_{label}_preview_{ts}.pdf"

    from src.cv_generator import generate_cv_pdf
    result = generate_cv_pdf(cv_data, path)
    ok(f"CV generado: {result}")


# ─── Command: cover-letter ────────────────────────────────────────────────────

def cmd_cl_list(args):
    from src.templates_manager import list_cover_letters, COVER_LETTERS_DIR

    letters = list_cover_letters()
    head("Cartas de presentación")
    if not letters:
        warn("No hay cartas — creá una con: python main.py cover-letter init")
        return
    for name in letters:
        path = COVER_LETTERS_DIR / f"{name}.txt"
        lines = len(path.read_text().splitlines())
        label = f"{'[genérica]' if name == 'generic' else '[nicho: ' + name + ']'}"
        print(f"  {c(GREEN,'✓')} {c(CYAN, name):<18} {c(DIM, label)}  {lines} líneas")
    print(f"\n  {c(DIM,'Editá cualquiera directamente en data/cover_letters/')}")


def cmd_cl_init(args):
    from src.templates_manager import (
        cover_letter_path, cover_letter_exists, COVER_LETTERS_DIR
    )

    COVER_LETTERS_DIR.mkdir(parents=True, exist_ok=True)
    niche = args.niche
    path  = cover_letter_path(niche)

    if path.exists() and not args.force:
        warn(f"Ya existe {path} — usá --force para sobreescribir")
        return

    # Use niche-aware template text
    templates = {
        "tech": "Estimado equipo de {company},\n\n[Presentación + interés en el rol de {position}]\n\n[Logro técnico relevante]\n\n[Por qué {company} específicamente]\n\nAdjunto CV. Quedo disponible para una entrevista técnica.\n\nSaludos,\n",
        "marketing": "Estimado equipo de {company},\n\n[Presentación + interés en {position}]\n\n[Campaña o resultado con métricas]\n\n[Por qué {company}]\n\nAdjunto CV.\n\nSaludos cordiales,\n",
        "finance": "Estimado equipo de {company},\n\n[Presentación + interés en {position}]\n\n[Logro financiero cuantificable]\n\n[Por qué {company}]\n\nAdjunto CV para su evaluación.\n\nAtentamente,\n",
        "data_science": "Estimado equipo de {company},\n\n[Presentación + interés en {position}]\n\n[Modelo implementado con impacto en el negocio]\n\n[Por qué {company}]\n\nAdjunto CV. Disponible para entrevista técnica.\n\nSaludos,\n",
        "hr": "Estimado equipo de {company},\n\n[Presentación + interés en {position}]\n\n[Iniciativa de RRHH con resultado concreto]\n\n[Por qué {company}]\n\nAdjunto CV.\n\nSaludos cordiales,\n",
    }
    default_template = "Estimado equipo de {company},\n\n[Presentación y motivo de interés en {position}]\n\n[Experiencia y logros relevantes]\n\n[Por qué {company} específicamente]\n\nAdjunto mi CV. Quedo disponible para una entrevista.\n\nSaludos cordiales,\n"
    content = templates.get(niche or "", default_template)

    path.write_text(content, encoding="utf-8")
    ok(f"Carta creada en {path}")
    print(f"  {c(BOLD,'Editá el archivo')} para completar los corchetes con tu información real.")
    print(f"  Variables disponibles: {{company}}, {{position}}, {{name}}")


def cmd_cl_preview(args):
    from src.templates_manager import load_cover_letter, which_cover_letter
    from src.cover_letter_generator import generate_cover_letter_pdf

    company  = args.company or "Empresa Ejemplo"
    position = args.position or "Puesto Ejemplo"
    niche    = args.niche

    base_cv = load_base_cv()
    candidate = base_cv.get("personal", {})
    name = candidate.get("name", "")

    try:
        content = load_cover_letter(niche, company, position, name)
        path_used, is_niche = which_cover_letter(niche)
        source = f"nicho '{niche}'" if is_niche else "genérica"
        info(f"Usando carta {source} ({path_used})")
    except FileNotFoundError as e:
        err(str(e)); sys.exit(1)

    ts     = datetime.now().strftime("%Y%m%d_%H%M")
    label  = niche or "generic"
    path   = Path("output/cover_letters") / f"Carta_{label}_preview_{ts}.pdf"

    result = generate_cover_letter_pdf(content, candidate, company, position, path)
    ok(f"Carta generada: {result}")


# ─── Command: apply ───────────────────────────────────────────────────────────

def cmd_apply(args):
    head(f"Nueva postulación: {args.position} @ {args.company}")

    # 1. Job description (optional — only needed for AI tailoring)
    job_description = ""
    if args.job_file:
        with open(args.job_file) as f:
            job_description = f.read().strip()
        ok(f"Descripción cargada desde {args.job_file}")
    elif args.ai:
        print(f"\n{c(BOLD,'Pegá la descripción del puesto')} (Enter dos veces para terminar):")
        lines, empty = [], 0
        while empty < 2:
            try:
                line = input()
            except EOFError:
                break
            if not line:
                empty += 1
            else:
                empty = 0
                lines.append(line)
        job_description = "\n".join(lines).strip()

    # 2. Detect niche
    from src.niche_manager import load_niche, list_niches, detect_niche_from_description
    from src.templates_manager import (
        niche_cv_exists, load_niche_cv,
        cover_letter_exists, load_cover_letter, which_cover_letter,
    )

    niche_id = args.niche
    if not niche_id:
        if job_description and os.environ.get("ANTHROPIC_API_KEY"):
            info("Detectando nicho con IA...")
            try:
                from src.ai_engine import suggest_niche
                niche_id = suggest_niche(job_description, list_niches())
                ok(f"Nicho detectado: {niche_id}")
            except Exception:
                niche_id = detect_niche_from_description(job_description) or "tech"
                warn(f"Nicho detectado por keywords: {niche_id}")
        elif job_description:
            niche_id = detect_niche_from_description(job_description) or "tech"
            warn(f"Nicho detectado por keywords: {niche_id}")
        else:
            niche_id = input(f"Ingresá el nicho {[n['id'] for n in list_niches()]}: ").strip()

    try:
        niche_data = load_niche(niche_id)
    except ValueError as e:
        err(str(e)); sys.exit(1)

    # 3. Choose CV source
    #    Priority: niche CV > AI tailoring > base CV
    if niche_cv_exists(niche_id):
        tailored_cv = load_niche_cv(niche_id)
        ok(f"Usando CV del nicho '{niche_id}'")
    elif job_description and os.environ.get("ANTHROPIC_API_KEY"):
        info("Adaptando CV base con IA...")
        try:
            from src.ai_engine import tailor_cv
            tailored_cv = tailor_cv(load_base_cv(), job_description, niche_data)
            ok("CV adaptado con IA")
        except Exception as e:
            warn(f"Error IA: {e}. Usando CV base.")
            tailored_cv = load_base_cv()
    else:
        tailored_cv = load_base_cv()
        if not niche_cv_exists(niche_id):
            warn(f"No hay CV para el nicho '{niche_id}'. "
                 f"Creá uno con: python main.py cv init-niche {niche_id}")

    # 4. Generate CV PDF
    slug = make_slug(args.company, args.position)
    ts   = datetime.now().strftime("%Y%m%d_%H%M")
    cv_path = Path("output/cvs") / f"CV_{slug}_{ts}.pdf"

    info("Generando PDF del CV...")
    from src.cv_generator import generate_cv_pdf
    cv_result = generate_cv_pdf(tailored_cv, cv_path)
    ok(f"CV: {cv_result}")

    # 5. Cover letter
    cl_path = None
    if args.cover_letter:
        # Priority: niche letter > generic letter > AI generation
        cl_path_out = Path("output/cover_letters") / f"Carta_{slug}_{ts}.pdf"
        candidate   = tailored_cv.get("personal", {})
        name        = candidate.get("name", "")

        if cover_letter_exists(niche_id) or cover_letter_exists(None):
            try:
                content    = load_cover_letter(niche_id, args.company, args.position, name)
                path_used, is_niche = which_cover_letter(niche_id)
                source = f"nicho '{niche_id}'" if is_niche else "genérica"
                info(f"Usando carta {source}")
                from src.cover_letter_generator import generate_cover_letter_pdf
                cl_result = generate_cover_letter_pdf(
                    content, candidate, args.company, args.position, cl_path_out
                )
                ok(f"Carta: {cl_result}")
                cl_path = cl_result
            except Exception as e:
                warn(f"Error al cargar carta: {e}")
        elif job_description and os.environ.get("ANTHROPIC_API_KEY"):
            info("Generando carta con IA...")
            try:
                from src.ai_engine import generate_cover_letter
                from src.cover_letter_generator import generate_cover_letter_pdf
                content   = generate_cover_letter(tailored_cv, job_description, args.company, args.position, niche_data)
                cl_result = generate_cover_letter_pdf(content, candidate, args.company, args.position, cl_path_out)
                ok(f"Carta (IA): {cl_result}")
                cl_path = cl_result
            except Exception as e:
                warn(f"Error al generar carta con IA: {e}")
        else:
            warn("No hay carta de presentación configurada. "
                 "Creá una con: python main.py cover-letter init")

    # 6. Send email
    contact_email = args.email
    if args.send_email:
        if not contact_email:
            contact_email = input("Email de destino: ").strip()
        if contact_email:
            info(f"Enviando a {contact_email}...")
            try:
                from src.email_sender import send_application
                name = tailored_cv.get("personal", {}).get("name", "")
                default_body = (
                    f"Estimado equipo de {args.company},\n\n"
                    f"Me postulo para el puesto de {args.position}. Adjunto mi CV."
                )
                send_application(
                    to_email=contact_email,
                    company=args.company,
                    position=args.position,
                    body=default_body,
                    cv_path=cv_result,
                    cover_letter_path=cl_path,
                    candidate_name=name,
                )
                ok(f"Email enviado a {contact_email}")
            except Exception as e:
                err(f"Error al enviar email: {e}")
        else:
            warn("Email no proporcionado. Omitiendo envío.")

    # 7. Track
    from src import tracker
    app_id = tracker.add_application(
        company=args.company,
        position=args.position,
        niche=niche_id,
        cv_path=str(cv_result),
        cover_letter_path=str(cl_path) if cl_path else None,
        job_url=args.job_url,
        contact_email=contact_email,
        notes=args.notes,
    )

    print()
    ok(f"Postulación registrada (ID: {app_id})")
    print(f"  Actualizá el estado: {c(CYAN, f'python main.py track update {app_id} --status entrevista')}")


# ─── Command: track ───────────────────────────────────────────────────────────

STATUS_COLORS = {
    "enviada": BLUE, "en_proceso": CYAN, "entrevista": YELLOW,
    "oferta": GREEN, "rechazada": RED, "descartada": DIM,
}
STATUSES = list(STATUS_COLORS.keys())


def cmd_track_list(args):
    from src import tracker
    apps = tracker.list_applications(
        niche=getattr(args, "niche", None),
        status=getattr(args, "status", None),
    )
    if not apps:
        warn("No hay postulaciones con esos filtros.")
        return

    head(f"Postulaciones ({len(apps)} total)")
    fmt = "  {:<4} {:<20} {:<24} {:<14} {:<12} {}"
    print(c(DIM, fmt.format("ID", "Empresa", "Puesto", "Nicho", "Estado", "Fecha")))
    print(c(DIM, "  " + "-" * 82))
    for app in apps:
        color = STATUS_COLORS.get(app["status"], "")
        print(fmt.format(
            str(app["id"]),
            app["company"][:20],
            app["position"][:24],
            app["niche"],
            c(color, app["status"]),
            app["applied_at"][:10],
        ))


def cmd_track_update(args):
    from src import tracker
    tracker.update_status(args.id, args.status, getattr(args, "notes", None))
    ok(f"Postulación {args.id} → '{args.status}'")


def cmd_track_stats(args):
    from src import tracker
    stats = tracker.get_stats()
    head("Estadísticas")
    print(f"  {c(BOLD,'Total:')} {stats['total']}")
    if stats["by_status"]:
        print(f"\n  {c(BOLD,'Por estado:')}")
        for s, cnt in sorted(stats["by_status"].items(), key=lambda x: -x[1]):
            color = STATUS_COLORS.get(s, "")
            print(f"    {c(color, f'{s:<12}')} {cnt:>3}  {c(color,'█'*cnt)}")
    if stats["by_niche"]:
        print(f"\n  {c(BOLD,'Por nicho:')}")
        for n, cnt in sorted(stats["by_niche"].items(), key=lambda x: -x[1]):
            print(f"    {c(CYAN, f'{n:<12}')} {cnt:>3}  {c(CYAN,'█'*cnt)}")


# ─── Parser ───────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Job Application Automation — Automatizá tus postulaciones con IA",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Verificar configuración")

    # niches
    p_niches = sub.add_parser("niches", help="Gestión de nichos")
    ns = p_niches.add_subparsers(dest="niches_cmd", required=True)
    ns.add_parser("list", help="Listar nichos")
    p_show = ns.add_parser("show", help="Ver detalles de un nicho")
    p_show.add_argument("niche_id")

    # cv
    p_cv = sub.add_parser("cv", help="Gestión de CVs por nicho")
    cv_sub = p_cv.add_subparsers(dest="cv_cmd", required=True)
    cv_sub.add_parser("list", help="Ver CVs disponibles por nicho")
    p_init = cv_sub.add_parser("init-niche", help="Crear CV para un nicho (copia desde base)")
    p_init.add_argument("niche_id", help="ID del nicho (ej: tech, marketing)")
    p_init.add_argument("--force", action="store_true", help="Sobreescribir si ya existe")
    p_prev = cv_sub.add_parser("preview", help="Generar PDF preview del CV")
    p_prev.add_argument("--niche", "-n", help="Nicho a previsualizar (usa base si no existe)")

    # cover-letter
    p_cl = sub.add_parser("cover-letter", help="Gestión de cartas de presentación")
    cl_sub = p_cl.add_subparsers(dest="cl_cmd", required=True)
    cl_sub.add_parser("list", help="Ver cartas disponibles")
    p_cl_init = cl_sub.add_parser("init", help="Crear carta de presentación")
    p_cl_init.add_argument("--niche", "-n", help="Para un nicho específico (omitir = genérica)")
    p_cl_init.add_argument("--force", action="store_true")
    p_cl_prev = cl_sub.add_parser("preview", help="Generar PDF preview de una carta")
    p_cl_prev.add_argument("--niche", "-n", help="Nicho (usa genérica si no se especifica)")
    p_cl_prev.add_argument("--company", "-c", default="Empresa Ejemplo")
    p_cl_prev.add_argument("--position", "-p", default="Puesto Ejemplo")

    # apply
    p_apply = sub.add_parser("apply", help="Postularse a un trabajo")
    p_apply.add_argument("--company",      "-c", required=True)
    p_apply.add_argument("--position",     "-p", required=True)
    p_apply.add_argument("--niche",        "-n", help="Nicho (auto-detecta si no se especifica)")
    p_apply.add_argument("--job-url",      "-u")
    p_apply.add_argument("--email",        "-e", dest="email")
    p_apply.add_argument("--cover-letter", "-cl", action="store_true")
    p_apply.add_argument("--send-email",   "-s",  action="store_true")
    p_apply.add_argument("--notes")
    p_apply.add_argument("--job-file",     "-f",  help="Archivo .txt con la descripción del puesto")
    p_apply.add_argument("--ai",           action="store_true",
                         help="Pedir descripción del puesto para tailoring con IA")

    # track
    p_track = sub.add_parser("track", help="Seguimiento de postulaciones")
    ts = p_track.add_subparsers(dest="track_cmd", required=True)
    p_tl = ts.add_parser("list")
    p_tl.add_argument("--niche",  "-n")
    p_tl.add_argument("--status", "-s", choices=STATUSES)
    p_tu = ts.add_parser("update")
    p_tu.add_argument("id", type=int)
    p_tu.add_argument("--status", "-s", choices=STATUSES, required=True)
    p_tu.add_argument("--notes",  "-n")
    ts.add_parser("stats")

    return parser


def main():
    load_env()
    parser = build_parser()
    args   = parser.parse_args()

    sub_cmd = (
        getattr(args, "niches_cmd", None)
        or getattr(args, "cv_cmd", None)
        or getattr(args, "cl_cmd", None)
        or getattr(args, "track_cmd", None)
    )

    dispatch = {
        ("init",          None):          cmd_init,
        ("niches",        "list"):        cmd_niches_list,
        ("niches",        "show"):        cmd_niches_show,
        ("cv",            "list"):        cmd_cv_list,
        ("cv",            "init-niche"):  cmd_cv_init_niche,
        ("cv",            "preview"):     cmd_cv_preview,
        ("cover-letter",  "list"):        cmd_cl_list,
        ("cover-letter",  "init"):        cmd_cl_init,
        ("cover-letter",  "preview"):     cmd_cl_preview,
        ("apply",         None):          cmd_apply,
        ("track",         "list"):        cmd_track_list,
        ("track",         "update"):      cmd_track_update,
        ("track",         "stats"):       cmd_track_stats,
    }

    fn = dispatch.get((args.command, sub_cmd))
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
