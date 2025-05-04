from PyQt6.QtCore import QObject, pyqtSignal
from solutions.bruteforce import brutforce


class BruteForceWokrer(QObject):
    rhomb_progress = pyqtSignal(int, int)
    square_progress = pyqtSignal(int, int)
    finished = pyqtSignal(object, object)

    def __init__(self, file):
        super().__init__()
        self.file = file

    def run(self):
        def on_rhomb(i, total):
            self.rhomb_progress.emit(i, total)

        def on_square(i, total):
            self.square_progress.emit(i, total)

        squares, rhombs = brutforce(self.file, on_rhomb, on_square)
        self.finished.emit(squares, rhombs)
