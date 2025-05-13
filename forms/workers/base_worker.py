import os
import time
from abc import ABC, abstractmethod

import psutil
from PyQt6.QtCore import QObject, pyqtSignal
from classes.point import Point
from solutions.solution_interface import SolutionInterface


class MetaQObject(type(QObject), type(ABC)):
    pass


class BaseWorker(QObject, ABC, metaclass=MetaQObject):

    progress = pyqtSignal(int, int)
    finished = pyqtSignal(object, object)
    stats = pyqtSignal(float, int)

    def __init__(self, solver: SolutionInterface, data: list[Point],
                 area: tuple[int, int] = None):
        super().__init__()
        self.solver = solver
        self.data = data
        self.area = area
        self.total_steps = 0
        self.current_step = 0

    @abstractmethod
    def configure_solver(self) -> SolutionInterface:
        pass

    def run(self):
        def report_progress(i, total):
            # Update total steps if this is the first progress report
            if self.total_steps == 0:
                self.total_steps = total * 2  # Double the total for both stages
            
            # If we're in the second half, adjust the progress
            if i > total:
                self.current_step = total + (i - total)
            else:
                self.current_step = i
            
            self.progress.emit(self.current_step, self.total_steps)

        start_time = time.perf_counter()
        process = psutil.Process(os.getpid())

        if self.area:
            squares, rhombs = self.solver.solve(
                self.data, self.area, on_progress=report_progress
            )
        else:
            squares, rhombs = self.solver.solve(
                self.data, area=None, on_progress=report_progress
            )

        elapsed = time.perf_counter() - start_time
        peak_memory = process.memory_info().rss

        # Emit results and statistics
        self.stats.emit(elapsed, peak_memory)
        self.finished.emit(squares, rhombs)

