from PyQt6.QtCore import QObject, pyqtSignal
from solutions.smort import smort


class SmortWorker(QObject):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(object, object)

    def __init__(self, file: str, area: tuple[int, int]):
        super().__init__()
        self.file = file
        self.area = area

    def run(self):
        def report(i, total):
            self.progress.emit(i, total)

        squares, rhombs = smort(self.file, self.area, report)
        self.finished.emit(squares, rhombs)
