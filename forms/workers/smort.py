from solutions.smort import Smart
from forms.workers.base_worker import BaseWorker
from classes.point import Point

class SmortWorker(BaseWorker):
    def __init__(self, data: list[Point], area: tuple[int, int]):
        super().__init__(solver=Smart(), data=data, area=area)

    def configure_solver(self):
        return Smart()
