import smtplib
from email.message import EmailMessage
from app.core.config import settings


def send_email(to_email: str, subject: str, text: str):
    message = EmailMessage()
    message["From"] = settings.EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(text)

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()  # TLS encryption
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.send_message(message)

    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email to {to_email}: {e}")