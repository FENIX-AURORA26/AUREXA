import sys
from PyQt5.QtWidgets import QApplication 
from ui.theme import aplicar_tema
from ui.login import Login
from ui.main_window import MainWindow

def abrir_main():
    global janela
    janela = MainWindow()
    janela.show()

app = QApplication(sys.argv)
aplicar_tema(app)

login = Login(abrir_main)
login.show()

sys.exit(app.exec_())