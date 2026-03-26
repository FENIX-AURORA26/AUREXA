from PyQt5.QtWidgets import QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget

from services.license import verificar_licenca


class Login(QWidget):
    def __init__(self, sucesso_callback):
        super().__init__()

        self.callback = sucesso_callback

        self.setWindowTitle("Login AUREXA")

        layout = QVBoxLayout()

        self.label = QLabel("Digite sua licença:")
        self.input = QLineEdit()
        self.input.setPlaceholderText("AUREXA-XXXX-XXX")

        self.botao = QPushButton("Entrar")
        self.botao.clicked.connect(self.verificar)

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.botao)

        self.setLayout(layout)

    def verificar(self):
        chave = self.input.text().strip()

        if not chave:
            QMessageBox.warning(self, "Licença", "Digite uma licença para continuar.")
            return

        resultado = verificar_licenca(chave)

        if resultado == "admin":
            QMessageBox.information(self, "Acesso liberado", "Acesso de administrador liberado.")
            self.callback()
            self.close()
            return

        if resultado == "user":
            QMessageBox.information(self, "Acesso liberado", "Usuário liberado com sucesso.")
            self.callback()
            self.close()
            return

        QMessageBox.critical(self, "Licença inválida", "A licença informada é inválida.")
