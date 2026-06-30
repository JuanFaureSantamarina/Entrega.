import os
import smtplib
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


def _load_settings() -> dict:
    with open("config/settings.yaml") as f:
        return yaml.safe_load(f)


def send_application(
    to_email: str,
    company: str,
    position: str,
    body: str,
    cv_path: Path,
    cover_letter_path=None,
    candidate_name: str = "",
) -> bool:
    """Send job application email with CV (and optionally cover letter) attached."""
    sender   = os.environ.get("EMAIL_SENDER", "")
    password = os.environ.get("EMAIL_PASSWORD", "")
    smtp_host = os.environ.get("EMAIL_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", "587"))

    if not sender or not password:
        raise RuntimeError(
            "EMAIL_SENDER y EMAIL_PASSWORD deben estar configurados en .env"
        )

    settings = _load_settings()
    subject_tpl = settings["email"]["default_subject"]
    subject = subject_tpl.format(position=position, company=company)
    signature = settings["email"]["signature"]
    full_body = f"{body}\n\n{signature}{candidate_name}"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(full_body, "plain", "utf-8"))

    def attach_file(path: Path, label: str):
        with open(path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{label}"')
        msg.attach(part)

    attach_file(cv_path, f"CV_{candidate_name.replace(' ', '_')}.pdf")
    if cover_letter_path and Path(cover_letter_path).exists():
        attach_file(
            cover_letter_path,
            f"CartaPresentacion_{candidate_name.replace(' ', '_')}.pdf",
        )

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())

    return True
