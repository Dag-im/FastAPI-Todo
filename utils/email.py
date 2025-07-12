import smtplib
from email.mime.text import MIMEText
from core.config import Settings

def send_email(to: str, subject: str, html_body: str):
    msg = MIMEText(html_body, "html")
    msg["Subject"] = subject
    msg["From"] = Settings.EMAIL_FROM
    msg["To"] = to

    with smtplib.SMTP(Settings.EMAIL_HOST, Settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(Settings.EMAIL_USER, Settings.EMAIL_PASSWORD)
        server.send_message(msg)
