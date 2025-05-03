import sys
from PyQt6.QtWidgets import (QMainWindow,
                             QApplication,
                             QPushButton,
                             QRadioButton,
                             QLabel,
                             QSpinBox,
                             QTextEdit,
                             QButtonGroup,)
from PyQt6.QtGui import QGuiApplication, QPixmap
from typing import cast


class MainUI(QMainWindow):
    def __init__(self) -> None:
        super(MainUI, self).__init__()
        self.setFixedSize(1200, 675)
        self.center()
        self.method: str = "brute"

        self.create_elements()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_elements(self) -> None:
        self.app_name_header: QLabel = QLabel(
            "Пошук ромбів та квадратів",
            self)
        self.app_name_header.setProperty("heading", True)

        self.solution_header: QLabel = QLabel(
            "Обреіть спосіб розв'язання",
            self)

        self.solution_metrics_header: QLabel = QLabel(
            "Метрики способу розв'язання",
            self)

        self.point_count_label: QLabel = QLabel(
            "Кількість точок для обрахунків",
            self)

        self.check_brute: QRadioButton = QRadioButton(
            "Повний перебір",
            self)
        self.check_brute.setChecked(True)

        self.check_smort: QRadioButton = QRadioButton(
            "Використовуючи векторну математику",
            self)

        # object name binding to be able to set category
        self.check_brute.setObjectName("brute")
        self.check_smort.setObjectName("smort")
        self.check_brute.toggled.connect(self.radio_button_handler)
        self.check_smort.toggled.connect(self.radio_button_handler)

        # radio buttons grouping
        self.method_group: QButtonGroup = QButtonGroup(self)
        self.method_group.addButton(self.check_brute)
        self.method_group.addButton(self.check_smort)

        # spin box config, changes depending on which method is selected
        self.point_count_sb: QSpinBox = QSpinBox(self)
        self.point_count_sb.setMinimum(0)
        self.point_count_sb.setMaximum(100)
        self.point_count_sb.valueChanged.connect(self.spin_box_handler)
        self.point_count_sb.setGeometry(100, 0, 200, 200)

        self.metrics: QTextEdit = QTextEdit(self)
        self.metrics.setDisabled(True)

        self.do_things_btn: QPushButton = QPushButton("Виконати", self)
        self.do_things_btn.setDisabled(True)

        self.result: QLabel = QLabel(self)
        self.result.setPixmap(QPixmap("style/assets/square.png"))

    def radio_button_handler(self) -> None:
        radio: QRadioButton = cast(QRadioButton, self.sender())
        if not radio.isChecked():
            return None

        match radio.objectName():
            case "brute":
                self.method = "brute"
                self.point_count_sb.setMaximum(100)
            case "smort":
                self.method = "smort"
                self.point_count_sb.setMaximum(1000)

        print(self.method)

    def spin_box_handler(self) -> None:
        spinbox: QSpinBox = cast(QSpinBox, self.sender())
        if spinbox.value() < 4:
            self.do_things_btn.setDisabled(True)
        else:
            self.do_things_btn.setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    with open("style/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window.show()
    app.exec()
