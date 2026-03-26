from unittest import result

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel 
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

    def abrir_painel_admin():
    print("PAINEL ADMIN AUREXA 🔥")
    
    
if result == "admin":
    print("👑 ACESSO DE DONA LIBERADO")
    abrir_painel_admin() 

elif result == "user":
    print("✅ USUÁRIO LIBERADO")
    abrir_app_normal()

else:
    print("❌ LICENÇA INVÁLIDA")