from PyQt6.QtCore import QObject, pyqtSignal
import time
import os
import psutil
from abc import ABC, abstractmethod
from solutions.solution_interface import SolutionInterface


class MetaQObject(type(QObject), type(ABC)):
    pass


class BaseWorker(QObject, ABC, metaclass=MetaQObject):

    progress = pyqtSignal(int, int)
    finished = pyqtSignal(object, object)
    stats = pyqtSignal(float, int)

    def __init__(self, solver: SolutionInterface, file: str, 
                 area: tuple[int, int] = None):
        super().__init__()
        self.solver = solver
        self.file = file
        self.area = area

    @abstractmethod
    def configure_solver(self) -> SolutionInterface:
        pass

    def run(self):
        def report_rhomb(i, total):
            self.progress.emit(i, total)

        def report_square(i, total):
            self.progress.emit(i + total, total * 2)

        start_time = time.perf_counter()
        process = psutil.Process(os.getpid())

        if self.area:
            squares, rhombs = self.solver.solve(self.file, self.area, 
                                                on_progress_rhomb=report_rhomb, 
                                                on_progress_square=report_square)
        else:
            squares, rhombs = self.solver.solve(self.file, 
                                                on_progress_rhomb=report_rhomb, 
                                                on_progress_square=report_square,
                                                area=None)

        elapsed = time.perf_counter() - start_time
        peak_memory = process.memory_info().rss

        # Emit results and statistics
        self.stats.emit(elapsed, peak_memory)
        self.finished.emit(squares, rhombs)

