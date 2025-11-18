
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


def send_email_with_template(to_addr: str,
                             template_path: str,
                             subject: str = "Notice",
                             smtp_env: str = "SMTP_SERVER") -> None:
    server = os.getenv(smtp_env)
    port = os.getenv("SMTP_PORT")
    from_addr = os.getenv("SMTP_FROM")
    if not all([server, port, from_addr]):
        raise EnvironmentError("Error: SMTP environment variables not fully set")

    tp = Path(template_path)
    if not tp.is_file():
        raise FileNotFoundError(f"Error: {template_path} is not a file")

    content = tp.read_text(encoding="utf-8").replace("{{name}}", to_addr)

    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(content)

    with smtplib.SMTP(server, int(port), timeout=5) as s:
        s.send_message(msg)
