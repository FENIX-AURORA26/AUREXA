import sys

from PyQt5.QtWidgets import QApplication

from ui.login import Login
from ui.main_window import MainWindow
from ui.theme import aplicar_tema


def main():
    app = QApplication(sys.argv)
    aplicar_tema(app)

    janela = {"main": None}

    def abrir_main():
        janela["main"] = MainWindow()
        janela["main"].show()

    login = Login(abrir_main)
    login.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
