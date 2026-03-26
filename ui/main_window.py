from PyQt5.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget  # type: ignore

from config import APP_NAME, SUPPORT_EMAIL
from core.optimizer import liberar_ram, limpar_cache
from services.ai import responder


class MainWindow(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.user = session["user"]

        self.setWindowTitle(APP_NAME)

        layout = QVBoxLayout()

        self.label = QLabel(f"Painel {APP_NAME}")
        self.user_label = QLabel(
            f"Usuario: {self.user['name']} | Email: {self.user['email']}"
        )
        self.plan_label = QLabel(
            f"Plano: {self.user['plan']} | Perfil: {self.user['role']} | "
            f"Licenca: {self.user['license_key']}"
        )
        self.support_label = QLabel(f"Suporte: {SUPPORT_EMAIL}")

        self.botao1 = QPushButton("Limpar Cache")
        self.botao2 = QPushButton("Liberar RAM")

        self.botao1.clicked.connect(self.cache)
        self.botao2.clicked.connect(self.ram)

        self.input_ai = QTextEdit()
        self.input_ai.setPlaceholderText("Pergunte para a IA sobre sistema, plano ou conta...")

        self.botao_ai = QPushButton("Perguntar IA")
        self.botao_ai.clicked.connect(self.perguntar)

        self.resposta = QLabel("")

        layout.addWidget(self.label)
        layout.addWidget(self.user_label)
        layout.addWidget(self.plan_label)
        layout.addWidget(self.support_label)
        layout.addWidget(self.botao1)
        layout.addWidget(self.botao2)
        layout.addWidget(self.input_ai)
        layout.addWidget(self.botao_ai)
        layout.addWidget(self.resposta)

        self.setLayout(layout)

    def cache(self):
        self.resposta.setText(limpar_cache())

    def ram(self):
        self.resposta.setText(liberar_ram())

    def perguntar(self):
        pergunta = self.input_ai.toPlainText()
        self.resposta.setText(
            responder(
                pergunta,
                plano=self.user["plan"],
                role=self.user["role"],
            )
        )
