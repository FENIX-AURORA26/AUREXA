import sys

from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NOVO_APP")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Base inicial para seu proximo app."))
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
