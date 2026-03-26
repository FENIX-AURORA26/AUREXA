import os
import smtplib
from email.mime.text import MIMEText

from config import APP_NAME, SUPPORT_EMAIL


def enviar_suporte(mensagem):
    email = os.getenv("AUREXA_SUPPORT_EMAIL")
    senha = os.getenv("AUREXA_SUPPORT_PASSWORD")

    if not email or not senha:
        raise RuntimeError(
            "Defina AUREXA_SUPPORT_EMAIL e AUREXA_SUPPORT_PASSWORD antes de enviar suporte."
        )

    msg = MIMEText(mensagem)
    msg["Subject"] = f"Suporte {APP_NAME}"
    msg["From"] = email
    msg["To"] = SUPPORT_EMAIL

    server = smtplib.SMTP_SSL("smtp.umbler.com", 465)
    server.login(email, senha)
    server.send_message(msg)
    server.quit()
