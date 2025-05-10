from solutions.smort import Smart
from forms.workers.base_worker import BaseWorker


class SmortWorker(BaseWorker):
    def __init__(self, file: str, area: tuple[int, int]):
        super().__init__(solver=Smart(), file=file, area=area)

    def configure_solver(self):
        return Smart()
