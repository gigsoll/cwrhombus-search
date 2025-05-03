import sys
from PyQt6.QtWidgets import (QMainWindow,
                             QWidget,
                             QApplication,
                             QPushButton,
                             QRadioButton,
                             QLabel,
                             QSpinBox,
                             QTextEdit,
                             QButtonGroup,
                             QVBoxLayout,
                             QHBoxLayout)
from PyQt6.QtGui import QGuiApplication, QPixmap
from typing import cast


class MainUI(QMainWindow):
    def __init__(self) -> None:
        super(MainUI, self).__init__()
        self.setFixedSize(1200, 675)
        self.center()
        self.method: str = "brute"

        self.create_elements()
        self.create_layout()

    def create_elements(self) -> None:
        self.app_name_header: QLabel = QLabel(
            "Пошук ромбів та квадратів",
            self)
        self.app_name_header.setProperty("heading", True)

        self.solution_header: QLabel = QLabel(
            "Обреіть спосіб розв'язання",
            self)
        self.solution_header.setProperty("heading2", True)

        self.solution_metrics_header: QLabel = QLabel(
            "Метрики способу розв'язання",
            self)
        self.solution_metrics_header.setProperty("heading2", True)

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

        self.metrics: QTextEdit = QTextEdit(self)
        self.metrics.setDisabled(True)

        self.do_things_btn: QPushButton = QPushButton("Виконати", self)
        self.do_things_btn.setDisabled(True)

        self.result: QLabel = QLabel(self)
        self.result.setPixmap(QPixmap("media/result.png"))

    def create_layout(self) -> None:
        self.sidebar = QWidget()
        self.checkbox_wraper = QWidget()
        self.point_count_wraper = QWidget()
        # define layouts
        self.main_layout: QHBoxLayout = QHBoxLayout()
        self.graph: QVBoxLayout = QVBoxLayout()
        self.point_count: QHBoxLayout = QHBoxLayout(self.point_count_wraper)
        self.point_count_wraper.setProperty("tint", True)
        self.sidebar_layout: QVBoxLayout = QVBoxLayout(self.sidebar)
        self.checkbox_wraper.setProperty("tint", True)
        self.radio: QVBoxLayout = QVBoxLayout(self.checkbox_wraper)

        # config main layout
        self.main: QWidget = QWidget(self)
        self.setCentralWidget(self.main)
        self.main.setLayout(self.main_layout)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addLayout(self.graph)

        # config point count
        self.point_count.addWidget(self.point_count_label)
        self.point_count.addWidget(self.point_count_sb)

        self.radio.addWidget(self.check_brute)
        self.radio.addWidget(self.check_smort)

        # config sidebar layout
        self.sidebar_layout.addWidget(self.app_name_header)
        self.sidebar_layout.addWidget(self.solution_header)
        self.sidebar_layout.addWidget(self.checkbox_wraper)
        self.sidebar_layout.addWidget(self.point_count_wraper)
        self.sidebar_layout.addWidget(self.solution_metrics_header)
        self.sidebar_layout.addWidget(self.metrics)
        self.sidebar_layout.addWidget(self.do_things_btn)
        self.main.setContentsMargins(15, 15, 15, 15)
        self.sidebar.setProperty("sidebar", True)

        # config graph layout
        self.graph.addWidget(self.result)



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

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    with open("style/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window.show()
    app.exec()
