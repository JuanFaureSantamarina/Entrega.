#!/usr/bin/env python3
"""
Job Application Automation CLI
Automatizá tus postulaciones laborales con IA (Claude).

Uso rápido:
  python main.py init
  python main.py apply --company "Empresa" --position "Desarrollador" --cover-letter
  python main.py track list
  python main.py niches list
"""

import argparse
import os
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path


# ─── Terminal colors (sin dependencias externas) ───────────────────────────────
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
    """Parse .env file manually (no python-dotenv needed)."""
    env_path = Path(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


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


def load_settings() -> dict:
    with open("config/settings.yaml") as f:
        return yaml.safe_load(f)


# ─── Command: init ────────────────────────────────────────────────────────────

def cmd_init(args):
    head("Verificando configuración...")

    env_path = Path(".env")
    if env_path.exists():
        ok(".env encontrado")
    else:
        warn("No hay .env — copiá .env.example a .env y completá tus credenciales")

    if os.environ.get("ANTHROPIC_API_KEY"):
        ok("ANTHROPIC_API_KEY configurada")
    else:
        err("ANTHROPIC_API_KEY no configurada (necesaria para IA)")

    cv_path = Path("data/base_cv.yaml")
    if cv_path.exists():
        base_cv = yaml.safe_load(cv_path.read_text())
        name = base_cv.get("personal", {}).get("name", "")
        if name and name != "Tu Nombre Completo":
            ok(f"CV base encontrado: {name}")
        else:
            warn("CV base existe pero no fue completado. Editá data/base_cv.yaml")
    else:
        err("No se encontró data/base_cv.yaml")

    from src.niche_manager import list_niches
    niches = list_niches()
    ok(f"{len(niches)} nichos: {', '.join(n['id'] for n in niches)}")

    for d in ["output/cvs", "output/cover_letters"]:
        Path(d).mkdir(parents=True, exist_ok=True)
    ok("Carpetas de output listas")

    print()
    print(c(BOLD+CYAN, "Uso básico:"))
    print(f"  python main.py apply --company 'Empresa' --position 'Puesto' --cover-letter")
    print(f"  python main.py track list")
    print(f"  python main.py niches list")


# ─── Command: niches ──────────────────────────────────────────────────────────

def cmd_niches_list(args):
    from src.niche_manager import list_niches
    niches = list_niches()
    if not niches:
        warn("No hay nichos configurados en config/niches/")
        return

    head("Nichos disponibles")
    col_id   = max(len(n["id"]) for n in niches) + 2
    col_name = max(len(n["name"]) for n in niches) + 2
    print(f"  {'ID':<{col_id}} {'Nombre':<{col_name}} Descripción")
    print(f"  {'-'*col_id} {'-'*col_name} {'-'*30}")
    for n in niches:
        print(f"  {c(CYAN, n['id']):<{col_id+9}} {c(BOLD, n['name']):<{col_name+4}} {n.get('description', '')}")


def cmd_niches_show(args):
    from src.niche_manager import load_niche
    try:
        niche = load_niche(args.niche_id)
    except ValueError as e:
        err(str(e)); sys.exit(1)

    head(f"Nicho: {args.niche_id}")
    print(f"  {c(BOLD, 'Nombre:')}       {niche['name']}")
    print(f"  {c(BOLD, 'Descripción:')}  {niche.get('description', '-')}")
    print(f"  {c(BOLD, 'Tono:')}         {niche.get('tone', '-')}")
    print(f"  {c(BOLD, 'Énfasis:')}      {niche.get('emphasis', '-')}")
    print(f"  {c(BOLD, 'Keywords:')}     {', '.join(niche.get('keywords', []))}")


# ─── Command: apply ───────────────────────────────────────────────────────────

def cmd_apply(args):
    head(f"Nueva postulación: {args.position} @ {args.company}")

    # 1. Job description
    job_description = ""
    if args.job_file:
        with open(args.job_file) as f:
            job_description = f.read().strip()
        ok(f"Descripción cargada desde {args.job_file}")
    else:
        print(f"\n{c(BOLD, 'Pegá la descripción del puesto')} (Enter dos veces para terminar):")
        lines = []
        empty = 0
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

    if not job_description:
        warn("Sin descripción de puesto. Se usará el CV base sin tailoring.")

    # 2. Detect niche
    from src.niche_manager import load_niche, list_niches, detect_niche_from_description
    niche_id = args.niche

    if not niche_id and job_description:
        info("Detectando nicho automáticamente...")
        try:
            from src.ai_engine import suggest_niche
            niche_id = suggest_niche(job_description, list_niches())
            ok(f"Nicho detectado por IA: {niche_id}")
        except Exception:
            niche_id = detect_niche_from_description(job_description) or "tech"
            warn(f"Nicho detectado por keywords: {niche_id}")
    elif not niche_id:
        niche_id = input(f"Ingresá el nicho {[n['id'] for n in list_niches()]}: ").strip()

    try:
        niche_data = load_niche(niche_id)
    except ValueError as e:
        err(str(e)); sys.exit(1)

    # 3. Load + tailor CV
    base_cv = load_base_cv()
    tailored_cv = base_cv

    if job_description:
        info("Adaptando CV con IA...")
        try:
            from src.ai_engine import tailor_cv
            tailored_cv = tailor_cv(base_cv, job_description, niche_data)
            ok("CV adaptado.")
        except Exception as e:
            warn(f"No se pudo adaptar con IA: {e}. Usando CV base.")

    # 4. Generate CV PDF
    slug = make_slug(args.company, args.position)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    cv_path = Path("output/cvs") / f"CV_{slug}_{ts}.pdf"

    info("Generando PDF del CV...")
    from src.cv_generator import generate_cv_pdf
    result_path = generate_cv_pdf(tailored_cv, cv_path)
    ok(f"CV generado: {result_path}")

    # 5. Cover letter (optional)
    cl_path = None
    if args.cover_letter:
        if not job_description:
            warn("Se necesita descripción del puesto para la carta. Omitiendo.")
        else:
            info("Generando carta de presentación...")
            try:
                from src.ai_engine import generate_cover_letter
                from src.cover_letter_generator import generate_cover_letter_pdf
                cl_content = generate_cover_letter(
                    tailored_cv, job_description, args.company, args.position, niche_data
                )
                cl_filename = f"CartaPresentacion_{slug}_{ts}.pdf"
                cl_path = Path("output/cover_letters") / cl_filename
                cl_result = generate_cover_letter_pdf(
                    cl_content,
                    tailored_cv.get("personal", {}),
                    args.company,
                    args.position,
                    cl_path,
                )
                ok(f"Carta generada: {cl_result}")
            except Exception as e:
                warn(f"No se pudo generar la carta: {e}")

    # 6. Send email (optional)
    contact_email = args.email
    if args.send_email:
        if not contact_email:
            contact_email = input("Email de destino (RRHH/empresa): ").strip()
        if not contact_email:
            warn("Email no proporcionado. Omitiendo envío.")
        else:
            print(f"\nCuerpo del email (Enter dos veces para terminar):")
            default_body = (
                f"Estimado equipo de {args.company},\n\n"
                f"Me dirijo a ustedes para postularme al puesto de {args.position}.\n"
                "Adjunto mi CV para su consideración.\n"
            )
            print(f"[Presioná Enter para usar el cuerpo por defecto o escribí el tuyo]")
            lines = []
            empty = 0
            try:
                first = input()
                if not first:
                    lines = [default_body]
                else:
                    lines.append(first)
                    while empty < 2:
                        line = input()
                        if not line:
                            empty += 1
                        else:
                            empty = 0
                            lines.append(line)
            except EOFError:
                lines = [default_body]

            body = "\n".join(lines) if lines[0] != default_body else default_body

            info(f"Enviando email a {contact_email}...")
            try:
                from src.email_sender import send_application
                candidate_name = tailored_cv.get("personal", {}).get("name", "")
                send_application(
                    to_email=contact_email,
                    company=args.company,
                    position=args.position,
                    body=body,
                    cv_path=result_path,
                    cover_letter_path=cl_path,
                    candidate_name=candidate_name,
                )
                ok(f"Email enviado a {contact_email}")
            except Exception as e:
                err(f"Error al enviar email: {e}")

    # 7. Track
    from src import tracker
    app_id = tracker.add_application(
        company=args.company,
        position=args.position,
        niche=niche_id,
        cv_path=str(result_path),
        cover_letter_path=str(cl_path) if cl_path else None,
        job_url=args.job_url,
        contact_email=contact_email,
        notes=args.notes,
    )

    print()
    print(c(BOLD+GREEN, f"Postulación registrada (ID: {app_id})"))
    print(f"  Actualizá el estado con: {c(CYAN, f'python main.py track update {app_id} --status entrevista')}")


# ─── Command: cv ──────────────────────────────────────────────────────────────

def cmd_cv_preview(args):
    base_cv = load_base_cv()
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    path = Path("output/cvs") / f"CV_preview_{ts}.pdf"

    info("Generando CV...")
    from src.cv_generator import generate_cv_pdf
    result = generate_cv_pdf(base_cv, path)
    ok(f"CV generado: {result}")


def cmd_cv_generate(args):
    from src.niche_manager import load_niche
    base_cv = load_base_cv()

    try:
        niche_data = load_niche(args.niche)
    except ValueError as e:
        err(str(e)); sys.exit(1)

    job_description = ""
    if args.job_file:
        with open(args.job_file) as f:
            job_description = f.read()

    tailored_cv = base_cv
    if job_description:
        info("Adaptando CV con IA...")
        try:
            from src.ai_engine import tailor_cv
            tailored_cv = tailor_cv(base_cv, job_description, niche_data)
            ok("CV adaptado.")
        except Exception as e:
            warn(f"Error IA: {e}. Usando CV base.")

    slug = make_slug(args.company, args.position)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    path = Path("output/cvs") / f"CV_{slug}_{ts}.pdf"

    from src.cv_generator import generate_cv_pdf
    result = generate_cv_pdf(tailored_cv, path)
    ok(f"CV generado: {result}")


# ─── Command: track ───────────────────────────────────────────────────────────

STATUS_COLORS = {
    "enviada": BLUE,
    "en_proceso": CYAN,
    "entrevista": YELLOW,
    "oferta": GREEN,
    "rechazada": RED,
    "descartada": DIM,
}

STATUSES = list(STATUS_COLORS.keys())


def cmd_track_list(args):
    from src import tracker
    apps = tracker.list_applications(
        niche=getattr(args, "niche", None),
        status=getattr(args, "status", None),
    )
    if not apps:
        warn("No hay postulaciones registradas con esos filtros.")
        return

    head(f"Postulaciones ({len(apps)} total)")
    w = {"id": 4, "company": 18, "position": 22, "niche": 12, "status": 10, "date": 10}
    fmt = (f"  {{:<{w['id']}}} {{:<{w['company']}}} {{:<{w['position']}}} "
           f"{{:<{w['niche']}}} {{:<{w['status']}}} {{}}")
    print(c(DIM, fmt.format("ID", "Empresa", "Puesto", "Nicho", "Estado", "Fecha")))
    print(c(DIM, "  " + "-" * (sum(w.values()) + 5 * 2)))

    for app in apps:
        color = STATUS_COLORS.get(app["status"], "")
        date  = app["applied_at"][:10]
        print(fmt.format(
            str(app["id"]),
            app["company"][:w["company"]],
            app["position"][:w["position"]],
            app["niche"],
            c(color, app["status"]),
            date,
        ))


def cmd_track_update(args):
    from src import tracker
    tracker.update_status(args.id, args.status, getattr(args, "notes", None))
    ok(f"Postulación {args.id} → '{args.status}'")


def cmd_track_stats(args):
    from src import tracker
    stats = tracker.get_stats()

    head("Estadísticas de postulaciones")
    print(f"  {c(BOLD, 'Total:')} {stats['total']}")

    if stats["by_status"]:
        print(f"\n  {c(BOLD, 'Por estado:')}")
        for status, count in sorted(stats["by_status"].items(), key=lambda x: -x[1]):
            bar = "█" * count
            color = STATUS_COLORS.get(status, "")
            print(f"    {c(color, f'{status:<12}')} {count:>3}  {c(color, bar)}")

    if stats["by_niche"]:
        print(f"\n  {c(BOLD, 'Por nicho:')}")
        for niche, count in sorted(stats["by_niche"].items(), key=lambda x: -x[1]):
            bar = "█" * count
            print(f"    {c(CYAN, f'{niche:<12}')} {count:>3}  {c(CYAN, bar)}")


# ─── CLI setup ────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Job Application Automation — Automatizá tus postulaciones con IA",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    sub.add_parser("init", help="Verificar configuración")

    # niches
    p_niches = sub.add_parser("niches", help="Gestión de nichos")
    ns = p_niches.add_subparsers(dest="niches_cmd", required=True)
    ns.add_parser("list", help="Listar nichos")
    p_show = ns.add_parser("show", help="Ver detalles de un nicho")
    p_show.add_argument("niche_id")

    # apply
    p_apply = sub.add_parser("apply", help="Postularse a un trabajo")
    p_apply.add_argument("--company",  "-c", required=True, help="Empresa")
    p_apply.add_argument("--position", "-p", required=True, help="Puesto")
    p_apply.add_argument("--niche",    "-n", help="ID del nicho (auto-detecta si no se especifica)")
    p_apply.add_argument("--job-url",  "-u", help="URL de la oferta laboral")
    p_apply.add_argument("--email",    "-e", dest="email", help="Email de RRHH")
    p_apply.add_argument("--cover-letter", "-cl", action="store_true", help="Generar carta de presentación")
    p_apply.add_argument("--send-email", "-s", action="store_true", help="Enviar email automáticamente")
    p_apply.add_argument("--notes",    help="Notas adicionales")
    p_apply.add_argument("--job-file", "-f", help="Archivo .txt con descripción del puesto")

    # cv
    p_cv = sub.add_parser("cv", help="Generar CV")
    cv_sub = p_cv.add_subparsers(dest="cv_cmd", required=True)
    cv_sub.add_parser("preview", help="Preview del CV base")
    p_cvgen = cv_sub.add_parser("generate", help="Generar CV tailorizado")
    p_cvgen.add_argument("--company",  "-c", required=True)
    p_cvgen.add_argument("--position", "-p", required=True)
    p_cvgen.add_argument("--niche",    "-n", required=True)
    p_cvgen.add_argument("--job-file", "-f", help="Archivo con descripción del puesto")

    # track
    p_track = sub.add_parser("track", help="Seguimiento de postulaciones")
    ts = p_track.add_subparsers(dest="track_cmd", required=True)
    p_tl = ts.add_parser("list", help="Listar postulaciones")
    p_tl.add_argument("--niche",  "-n", help="Filtrar por nicho")
    p_tl.add_argument("--status", "-s", choices=STATUSES, help="Filtrar por estado")
    p_tu = ts.add_parser("update", help="Actualizar estado de postulación")
    p_tu.add_argument("id", type=int, help="ID de la postulación")
    p_tu.add_argument("--status", "-s", choices=STATUSES, required=True)
    p_tu.add_argument("--notes",  "-n", help="Notas")
    ts.add_parser("stats", help="Estadísticas")

    return parser


def main():
    load_env()
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        ("init",   None,       None):        cmd_init,
        ("niches", "list",     None):        cmd_niches_list,
        ("niches", "show",     None):        cmd_niches_show,
        ("apply",  None,       None):        cmd_apply,
        ("cv",     "preview",  None):        cmd_cv_preview,
        ("cv",     "generate", None):        cmd_cv_generate,
        ("track",  "list",     None):        cmd_track_list,
        ("track",  "update",   None):        cmd_track_update,
        ("track",  "stats",    None):        cmd_track_stats,
    }

    key = (
        args.command,
        getattr(args, "niches_cmd", None) or getattr(args, "cv_cmd", None) or getattr(args, "track_cmd", None),
        None,
    )
    fn = dispatch.get(key)
    if fn:
        fn(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
