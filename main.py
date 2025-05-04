from forms.main_ui import MainUI
import sys
from PyQt6.QtWidgets import QApplication


app = QApplication(sys.argv)
window = MainUI()
with open("style/style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)
window.show()
app.exec()
