from PyQt6.QtCore import QObject, pyqtSignal
from solutions.bruteforce import brutforce


class BrutforceWorker(QObject):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(object, object)

    def __init__(self, file: str):
        super().__init__()
        self.file = file

    def run(self):
        def report(i, total):
            self.progress.emit(i, total)

        squares, rhombs = brutforce(self.file, on_progress_rhomb=report)
        self.finished.emit(squares, rhombs)
