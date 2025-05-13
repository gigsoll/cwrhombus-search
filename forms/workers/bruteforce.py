from solutions.bruteforce import BrutForce
from forms.workers.base_worker import BaseWorker
from classes.point import Point

class BrutforceWorker(BaseWorker):
    def __init__(self, data: list[Point]):
        super().__init__(solver=BrutForce(), data=data)

    def configure_solver(self):
        return BrutForce()
