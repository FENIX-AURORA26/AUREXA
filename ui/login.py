from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel # type: ignore
from services.license import verificar_licenca

class Login(QWidget):
    def __init__(self, sucesso_callback):
        super().__init__()

        self.callback = sucesso_callback

        self.setWindowTitle("Login AUREXA")

        layout = QVBoxLayout()

        self.label = QLabel("Digite sua licença:")
        self.input = QLineEdit()
        self.botao = QPushButton("Entrar")

        self.botao.clicked.connect(self.verificar)

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.botao)

        self.setLayout(layout)

    def verificar(self):
        chave = self.input.text()

        if verificar_licenca(chave):
            self.callback()
            self.close()
        else:
            self.label.setText("Licença inválida!")