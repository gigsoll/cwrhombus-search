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
                             QHBoxLayout,
                             QCheckBox,
                             QProgressBar,)
from PyQt6.QtGui import QGuiApplication, QPixmap
from PyQt6.QtCore import QThread
from forms.workers.bruteforce import BrutforceWorker
from forms.workers.smort import SmortWorker
from typing import cast
from classes.point import point_reader
from forms.workers.graph import plot_data


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

        self.generation_settings: QLabel = QLabel(
            "Параметри створення випадкових точок",
            self)
        self.generation_settings.setProperty("heading2", True)

        self.solution_metrics_header: QLabel = QLabel(
            "Метрики способу розв'язання",
            self)
        self.solution_metrics_header.setProperty("heading2", True)

        self.point_count_label: QLabel = QLabel(
            "Кількість точок для обрахунків",
            self)

        self.point_min_label: QLabel = QLabel(
            "Мінімальне значення X та Y    ",
            self
        )

        self.point_max_label: QLabel = QLabel(
            "Максимальне значення X та Y ",
            self
        )

        self.check_brute: QRadioButton = QRadioButton(
            "Повний перебір",
            self)
        self.check_brute.setChecked(True)

        self.check_smort: QRadioButton = QRadioButton(
            "Використовуючи векторну математику",
            self)

        self.check_regenerate: QCheckBox = QCheckBox(
            "Створити новий набір точок",
            self
        )

        self.progressbar_label: QLabel = QLabel(
            "Процес виконання",
            self
        )

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
        self.point_min_sb: QSpinBox = QSpinBox(self)
        self.point_max_sb: QSpinBox = QSpinBox(self)
        self.point_min_sb.setMinimum(0)
        self.point_max_sb.setMinimum(0)
        self.point_count_sb.setMinimum(0)
        self.point_count_sb.setMaximum(100)
        self.point_min_sb.setMaximum(150)
        self.point_max_sb.setMaximum(150)
        self.point_count_sb.valueChanged.connect(self.spin_box_handler)

        self.metrics: QTextEdit = QTextEdit(self)
        self.metrics.setDisabled(True)

        self.do_things_btn: QPushButton = QPushButton("Виконати", self)
        self.do_things_btn.setDisabled(True)

        self.result: QLabel = QLabel(self)
        self.result.setPixmap(QPixmap("media/result.png"))

        self.progresbar: QProgressBar = QProgressBar(self)

    def create_layout(self) -> None:
        # wrapers
        self.sidebar = QWidget()
        self.checkbox_wraper = QWidget()
        self.point_info_wraper = QWidget()
        self.metrics_wraper = QWidget()

        # define layouts
        self.main_layout: QHBoxLayout = QHBoxLayout()
        self.progresbar_grouping: QHBoxLayout = QHBoxLayout()
        self.graph: QVBoxLayout = QVBoxLayout()
        self.point_min: QHBoxLayout = QHBoxLayout()
        self.point_max: QHBoxLayout = QHBoxLayout()
        self.point_count: QHBoxLayout = QHBoxLayout()
        self.properties: QVBoxLayout = QVBoxLayout(self.point_info_wraper)
        self.point_info_wraper.setProperty("tint", True)
        self.sidebar_layout: QVBoxLayout = QVBoxLayout(self.sidebar)
        self.checkbox_wraper.setProperty("tint", True)
        self.radio: QVBoxLayout = QVBoxLayout(self.checkbox_wraper)
        self.metrics_group: QVBoxLayout = QVBoxLayout(self.metrics_wraper)
        self.metrics_wraper.setProperty("tint", True)

        # config main layout
        self.main: QWidget = QWidget(self)
        self.setCentralWidget(self.main)
        self.main.setLayout(self.main_layout)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addLayout(self.graph)

        # config point count
        self.point_count.addWidget(self.point_count_label)
        self.point_count.addWidget(self.point_count_sb)

        # config point min max
        self.point_min.addWidget(self.point_min_label)
        self.point_min.addWidget(self.point_min_sb)
        self.point_max.addWidget(self.point_max_label)
        self.point_max.addWidget(self.point_max_sb)

        # add point info into wraper
        self.properties.addLayout(self.point_count)
        self.properties.addLayout(self.point_min)
        self.properties.addLayout(self.point_max)
        self.properties.addWidget(self.check_regenerate)

        self.radio.addWidget(self.check_brute)
        self.radio.addWidget(self.check_smort)

        self.progresbar_grouping.addWidget(self.progressbar_label)
        self.progresbar_grouping.addWidget(self.progresbar)

        # metrics wraper
        self.metrics_group.addLayout(self.progresbar_grouping)
        self.metrics_group.addWidget(self.metrics)

        # config sidebar layout
        self.sidebar_layout.addWidget(self.app_name_header)
        self.sidebar_layout.addWidget(self.solution_header)
        self.sidebar_layout.addWidget(self.checkbox_wraper)
        self.sidebar_layout.addWidget(self.generation_settings)
        self.sidebar_layout.addWidget(self.point_info_wraper)
        self.sidebar_layout.addWidget(self.solution_metrics_header)
        self.sidebar_layout.addWidget(self.metrics_wraper)
        self.sidebar_layout.addWidget(self.do_things_btn)
        self.main.setContentsMargins(0, 10, 10, 10)
        self.sidebar.setProperty("sidebar", True)
        self.sidebar.setProperty("drop_shadow", True)

        self.progresbar.setValue(43)

        # config graph layout
        self.graph.addWidget(self.result)

        self.do_things_btn.clicked.connect(self.start_task)

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

    def start_task(self):
        file = "dots.json"
        area = (self.point_min_sb.value(),
                self.point_max_sb.value())

        self.thread = QThread()

        if self.method == "brute":
            self.worker = BrutforceWorker(file)
        elif self.method == "smort":
            self.worker = SmortWorker(file, area)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.task_finished)
        self.worker.stats.connect(self.show_metrics)  # <== Connect metrics signal here

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.do_things_btn.setEnabled(False)
        self.thread.start()

    def update_progress(self, done, total):
        self.progresbar.setMaximum(total)
        self.progresbar.setValue(done)

    def task_finished(self, squares, rhombs):
        print(squares, rhombs)
        self.do_things_btn.setEnabled(True)
        points = point_reader("dots.json")
        plot_data(squares, rhombs, points)
        self.result.setPixmap(QPixmap("media/result.png"))

    def show_metrics(self, elapsed_time: float, peak_memory: int) -> None:
        time_msg = f"⏱ Elapsed Time: {elapsed_time:.3f} seconds"
        mem_msg = f"🧠 Peak Memory: {peak_memory / (1024 * 1024):.3f} MB"
        self.metrics.setPlainText(f"{time_msg}\n{mem_msg}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    with open("style/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window.show()
    app.exec()
