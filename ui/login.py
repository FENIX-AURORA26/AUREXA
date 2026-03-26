from PyQt5.QtWidgets import QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget

from config import APP_NAME, SUPPORT_EMAIL
from services.api_client import ApiClient, ApiClientError
from services.connection_diagnostic import diagnosticar_e_corrigir_api
from services.license import verificar_licenca


class Login(QWidget):
    def __init__(self, sucesso_callback):
        super().__init__()

        self.callback = sucesso_callback
        self.client = ApiClient()

        self.setWindowTitle(f"Login {APP_NAME}")
        self.resize(640, 560)

        layout = QVBoxLayout()

        self.label = QLabel(f"Entrar no {APP_NAME} // Painel Inteligente")
        self.label.setStyleSheet("font-size: 24px; font-weight: 700;")
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Senha")
        self.password.setEchoMode(QLineEdit.Password)

        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("Licenca (opcional)")

        self.info = QLabel(
            "Planos: free, premium, pro e owner. "
            "Use 'Corrigir conexao' se API cair. "
            f"Suporte: {SUPPORT_EMAIL}"
        )
        self.info.setWordWrap(True)

        self.botao = QPushButton("Entrar")
        self.botao.clicked.connect(self.verificar)

        self.botao_corrigir = QPushButton("Corrigir conexao")
        self.botao_corrigir.clicked.connect(self.corrigir_conexao)

        layout.addWidget(self.label)
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.license_input)
        layout.addWidget(self.info)
        layout.addWidget(self.botao)
        layout.addWidget(self.botao_corrigir)

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
            QMessageBox.critical(
                self,
                "API indisponivel",
                f"{erro}\n\n"
                "Passos para corrigir:\n"
                "1) Verifique internet e firewall.\n"
                "2) Confirme AUREXA_API_BASE_URL.\n"
                "3) Rode API local com: python server.py",
            )
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


    def corrigir_conexao(self):
        resultado = diagnosticar_e_corrigir_api()
        if resultado.get("status") == "ok":
            QMessageBox.information(self, "Conexao", resultado.get("message", "API online."))
        else:
            QMessageBox.critical(
                self,
                "Conexao",
                resultado.get("message", "Nao foi possivel corrigir automaticamente."),
            )
