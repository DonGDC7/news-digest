import smtplib
from datetime import date
from email.message import EmailMessage

from config import load_config

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(subject: str, body: str) -> None:
    config = load_config()
    address = config["GMAIL_ADDRESS"]
    password = config["GMAIL_APP_PASSWORD"].replace(" ", "")
    recipient = config["RECIPIENT_EMAIL"]
    missing = [
        name
        for name, value in (
            ("GMAIL_ADDRESS", address),
            ("GMAIL_APP_PASSWORD", password),
            ("RECIPIENT_EMAIL", recipient),
        )
        if not value
    ]
    if missing:
        raise RuntimeError("configuration email incomplète : " + ", ".join(missing))

    message = EmailMessage()
    message["From"] = address
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(address, password)
            smtp.send_message(message)
    except smtplib.SMTPServerDisconnected as error:
        raise RuntimeError(
            "Gmail a fermé la connexion au moment de l'identification. "
            "Vérifie que le mot de passe d'application correspond à GMAIL_ADDRESS."
        ) from error
    except smtplib.SMTPAuthenticationError as error:
        raise RuntimeError(
            "Gmail a refusé l'identification. "
            "Vérifie le mot de passe d'application."
        ) from error


def digest_body(items: list[dict[str, str]]) -> str:
    sections = []
    for item in items:
        summary = item["summary"] or "résumé indisponible"
        sections.append(
            f"{item['title']}\n"
            f"Source : {item['source']}\n\n"
            f"{summary}\n\n"
            f"{item['link']}"
        )
    return "\n\n---\n\n".join(sections)


def send_digest(items: list[dict[str, str]]) -> None:
    subject = f"Résumé des news du {date.today().strftime('%d/%m/%Y')}"
    send_email(subject, digest_body(items))
    print("email envoyé")


def send_test_email() -> None:
    send_email("test news-digest", "test news-digest")
    print("email de test envoyé")


if __name__ == "__main__":
    try:
        send_test_email()
    except Exception as error:
        print(f"envoi impossible ({error})")
