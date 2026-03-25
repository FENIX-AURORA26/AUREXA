from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel # type: ignore
from core.optimizer import limpar_cache, liberar_ram
from services.ai import responder

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AUREXA CORE")

        layout = QVBoxLayout()

        self.label = QLabel("Painel AUREXA")

        self.botao1 = QPushButton("Limpar Cache")
        self.botao2 = QPushButton("Liberar RAM")

        self.botao1.clicked.connect(self.cache)
        self.botao2.clicked.connect(self.ram)

        self.input_ai = QTextEdit()
        self.input_ai.setPlaceholderText("Pergunte para a IA...")

        self.botao_ai = QPushButton("Perguntar IA")
        self.botao_ai.clicked.connect(self.perguntar)

        self.resposta = QLabel("")

        layout.addWidget(self.label)
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
        self.resposta.setText(responder(pergunta))