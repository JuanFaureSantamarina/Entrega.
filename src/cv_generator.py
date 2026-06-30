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


def _fmt_date(date_str) -> str:
    if not date_str:
        return "Presente"
    try:
        dt = datetime.strptime(str(date_str), "%Y-%m")
        months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                  "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        return f"{months[dt.month - 1]} {dt.year}"
    except Exception:
        return str(date_str)


def generate_cv_html(cv_data: dict) -> str:
    env = Environment(loader=FileSystemLoader("templates"))
    env.filters["fmt_date"] = _fmt_date
    tmpl = env.get_template("cv.html")
    return tmpl.render(cv=cv_data)


def generate_cv_pdf(cv_data: dict, output_path: Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html_content = generate_cv_html(cv_data)

    # Write temp HTML
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

    # Fallback: keep HTML if PDF generation fails
    fallback = output_path.with_suffix(".html")
    if not fallback.exists():
        fallback.write_text(html_content, encoding="utf-8")
    return fallback
