from PyQt5.QtWidgets import QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget # type: ignore

from config import APP_NAME, SUPPORT_EMAIL
from services.api_client import ApiClient, ApiClientError
from services.license import verificar_licenca


class Login(QWidget):
    def __init__(self, sucesso_callback):
        super().__init__()

        self.callback = sucesso_callback
        self.client = ApiClient()

        self.setWindowTitle(f"Login {APP_NAME}")

        layout = QVBoxLayout()

        self.label = QLabel(f"Entrar no {APP_NAME}")
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Senha")
        self.password.setEchoMode(QLineEdit.Password)

        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("Licenca (opcional)")

        self.info = QLabel(
            "Planos disponiveis: free, premium, pro e owner. "
            f"Suporte: {SUPPORT_EMAIL}"
        )

        self.botao = QPushButton("Entrar")
        self.botao.clicked.connect(self.verificar)

        layout.addWidget(self.label)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.license_input)
        layout.addWidget(self.info)
        layout.addWidget(self.botao)

        self.setLayout(layout)

    def verificar(self):
        email = self.email.text().strip()
        senha = self.password.text().strip()
        chave = self.license_input.text().strip()

        if not email or not senha:
            QMessageBox.warning(self, "Login", "Digite email e senha para continuar.")
            return

        try:
            resposta = self.client.login(email, senha)
        except ApiClientError as erro:
            QMessageBox.critical(self, "API indisponivel", str(erro))
            return

        if resposta.get("status") != "ok":
            QMessageBox.critical(self, "Login", resposta.get("message", "Falha no login."))
            return

        if chave:
            resultado = verificar_licenca(email, chave)
            if not resultado:
                QMessageBox.critical(
                    self,
                    "Licenca invalida",
                    "A licenca informada nao corresponde a sua conta.",
                )
                return

        session = resposta["session"]
        role = session["user"]["role"]
        plan = session["user"]["plan"]

        if role == "owner":
            mensagem = "Acesso total owner liberado."
        else:
            mensagem = f"Acesso liberado para o plano {plan}."

        QMessageBox.information(self, "Acesso liberado", mensagem)
        self.callback(session)
        self.close()
