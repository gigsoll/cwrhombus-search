from dataclasses import dataclass
from .rhombus import Rhombus
from .exceptions import NotASquare


@dataclass
class Square(Rhombus):
    def __post_init__(self):
        diag_lengths = self.calculate_diagonals()
        if diag_lengths[0] != diag_lengths[1]:
            raise NotASquare("Diagonals have different length,"
                             "so it isn't a Square")
