import smtplib
from email.mime.text import MIMEText

def enviar_suporte(mensagem):
    email = "luna_site@fenix-boreal.com.br"
    senha = "SENHA_EMAIL"

    msg = MIMEText(mensagem)
    msg["Subject"] = "Suporte AUREXA"
    msg["From"] = email
    msg["To"] = "suporte@fenix-boreal.com.br"

    server = smtplib.SMTP_SSL("smtp.umbler.com", 465)
    server.login(email, senha)
    server.send_message(msg)
    server.quit()