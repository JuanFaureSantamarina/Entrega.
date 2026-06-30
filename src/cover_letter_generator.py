import subprocess
import shutil
import glob as _glob
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


CHROMIUM_CANDIDATES = [
    "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
    "/usr/bin/google-chrome",
]


def _find_chromium() -> str | None:
    for pattern in CHROMIUM_CANDIDATES:
        matches = _glob.glob(pattern)
        if matches:
            return matches[0]
    return shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")


def _today_es() -> str:
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    now = datetime.now()
    return f"{now.day} de {months[now.month - 1]} de {now.year}"


def generate_cover_letter_html(
    content: str,
    candidate: dict,
    company: str,
    position: str,
) -> str:
    env = Environment(loader=FileSystemLoader("templates"))
    tmpl = env.get_template("cover_letter.html")
    return tmpl.render(
        content=content,
        candidate=candidate,
        company=company,
        position=position,
        today=_today_es(),
        paragraphs=[p.strip() for p in content.split("\n\n") if p.strip()],
    )


def generate_cover_letter_pdf(
    content: str,
    candidate: dict,
    company: str,
    position: str,
    output_path: Path,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_content = generate_cover_letter_html(content, candidate, company, position)
    html_path = output_path.with_suffix(".html")
    html_path.write_text(html_content, encoding="utf-8")

    chromium = _find_chromium()
    if chromium:
        try:
            result = subprocess.run(
                [
                    chromium,
                    "--headless=new",
                    "--no-sandbox",
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    f"--print-to-pdf={output_path}",
                    "--print-to-pdf-no-header",
                    str(html_path),
                ],
                capture_output=True,
                timeout=30,
            )
            if output_path.exists():
                html_path.unlink(missing_ok=True)
                return output_path
        except Exception:
            pass

    fallback = output_path.with_suffix(".html")
    if not fallback.exists():
        fallback.write_text(html_content, encoding="utf-8")
    return fallback
