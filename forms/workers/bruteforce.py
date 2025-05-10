from solutions.bruteforce import BrutForce
from forms.workers.base_worker import BaseWorker


class BrutforceWorker(BaseWorker):
    def __init__(self, file: str):
        super().__init__(solver=BrutForce(), file=file)

    def configure_solver(self):
        return BrutForce()
