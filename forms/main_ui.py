import sys
import time
from typing import List, cast

from PyQt6.QtCore import QThread
from PyQt6.QtGui import QGuiApplication, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from classes.point import Point, point_reader, point_writer
from forms.workers.bruteforce import BrutforceWorker
from forms.workers.graph import plot_data
from forms.workers.smort import SmortWorker
from generate_points import generate_points


class MainUI(QMainWindow):
    def __init__(self) -> None:
        super(MainUI, self).__init__()
        self.setFixedSize(1200, 675)
        self.center()
        self.method: str = "brute"
        self.points: List[Point] = []
        self.DOTS_FILE = "dots.json"
        self.squares: List[Point] = []
        self.rhombs: List[Point] = []
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
        self.point_max_sb: QSpinBox = QSpinBox(self)
        self.point_max_sb.setMinimum(0)
        self.point_count_sb.setMinimum(0)
        self.point_count_sb.setMaximum(100)
        self.point_max_sb.setMaximum(150)
        self.point_count_sb.valueChanged.connect(self.spin_box_handler)

        # Point management buttons
        self.generate_btn = QPushButton("Згенерувати точки", self)
        self.open_btn = QPushButton("Відкрити точки", self)
        self.save_btn = QPushButton("Зберегти точки", self)

        self.metrics: QTextEdit = QTextEdit(self)
        self.metrics.setDisabled(False)

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
        self.point_max: QHBoxLayout = QHBoxLayout()
        self.point_count: QHBoxLayout = QHBoxLayout()
        self.properties: QVBoxLayout = QVBoxLayout(self.point_info_wraper)
        self.point_info_wraper.setProperty("tint", True)
        self.sidebar_layout: QVBoxLayout = QVBoxLayout(self.sidebar)
        self.checkbox_wraper.setProperty("tint", True)
        self.radio: QVBoxLayout = QVBoxLayout(self.checkbox_wraper)
        self.metrics_group: QVBoxLayout = QVBoxLayout(self.metrics_wraper)
        self.metrics_wraper.setProperty("tint", True)
        self.file_buttons: QHBoxLayout = QHBoxLayout()

        # config main layout
        self.main: QWidget = QWidget(self)
        self.setCentralWidget(self.main)
        self.main.setLayout(self.main_layout)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addLayout(self.graph)

        # config point count
        self.point_count.addWidget(self.point_count_label)
        self.point_count.addWidget(self.point_count_sb)

        # config point max
        self.point_max.addWidget(self.point_max_label)
        self.point_max.addWidget(self.point_max_sb)

        # config file buttons
        self.file_buttons.addWidget(self.generate_btn)
        self.file_buttons.addWidget(self.open_btn)
        self.file_buttons.addWidget(self.save_btn)

        # add point info into wraper
        self.properties.addLayout(self.point_count)
        self.properties.addLayout(self.point_max)
        self.properties.addLayout(self.file_buttons)

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

        # config graph layout
        self.graph.addWidget(self.result)

        # Connect signals
        self.do_things_btn.clicked.connect(self.start_task)
        self.generate_btn.clicked.connect(self.generate_new_points)
        self.open_btn.clicked.connect(self.open_points)
        self.save_btn.clicked.connect(self.save_points)

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
        area = (0, self.point_max_sb.value())
        self.start_time = time.time()  # Store start time

        self.thread = QThread()

        if self.method == "brute":
            self.worker = BrutforceWorker(self.points)
        elif self.method == "smort":
            self.worker = SmortWorker(self.points, area)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.task_finished)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.do_things_btn.setEnabled(False)
        self.thread.start()

    def update_progress(self, done, total):
        self.progresbar.setMaximum(total)
        self.progresbar.setValue(done)

    def task_finished(self, squares, rhombs):
        self.squares = squares
        self.rhombs = rhombs
        print(self.squares)
        print(self.rhombs)
        self.do_things_btn.setEnabled(True)
        plot_data(self.squares, self.rhombs, self.points)
        self.result.setPixmap(QPixmap("media/result.png"))
        
        # Calculate and show execution time
        elapsed_time = time.time() - self.start_time
        self.metrics.setPlainText(
            f"⏱ Час виконання: {elapsed_time:.3f} секунд\n"
            f"Квадрати: {self.squares}\n"
            f"Ромби: {self.rhombs}")

    def generate_new_points(self) -> None:
        count = self.point_count_sb.value()
        max_coord = self.point_max_sb.value()
        try:
            generate_points((0, max_coord), count, self.DOTS_FILE)
            points = point_reader(self.DOTS_FILE)
            if isinstance(points, list):
                self.points = points
                plot_data([], [], self.points)
                self.result.setPixmap(QPixmap("media/result.png"))
                self.do_things_btn.setEnabled(True)
        except Exception as e:
            print(f"Error generating points: {e}")

    def open_points(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Відкрити файл з точками",
            "",
            "JSON Files (*.json)"
        )
        if file_name:
            try:
                points = point_reader(file_name)
                self.points = points
                plot_data([], [], self.points)
                self.result.setPixmap(QPixmap("media/result.png"))
                self.do_things_btn.setEnabled(True)
            except Exception as e:
                print(f"Error opening file: {e}")

    def save_points(self) -> None:
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Зберегти точки",
            "",
            "JSON Files (*.json)"
        )
        if file_name and self.points:
            point_writer(file_name, self.points)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    with open("style/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window.show()
    app.exec()
