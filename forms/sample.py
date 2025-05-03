from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("forms/sample.ui", self)


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    with open("style/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    app.exec()


if __name__ == '__main__':
    main()
