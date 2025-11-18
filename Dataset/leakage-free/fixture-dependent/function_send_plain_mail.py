import smtplib
from email.message import EmailMessage

def send_plain_email(to_addr: str, msg: str) -> None:
    email = EmailMessage()
    email.set_content(msg)
    email["Subject"] = "Test"
    email["From"] = "noreply@example.com"
    email["To"] = to_addr

    with smtplib.SMTP("localhost", 1025, timeout=5) as s:
        s.send_message(email)
