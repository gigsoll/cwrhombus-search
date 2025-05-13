from dataclasses import dataclass
from .rhombus import Rhombus
from .exceptions import NotASquare


@dataclass
class Square(Rhombus):
    def __repr__(self, emoji: str = "🟥") -> str:
        return f"{emoji} {self.point1}, {self.point2}, {self.point3}, {self.point4}"

    def __post_init__(self):
        diag_lengths = self.calculate_diagonals()
        if diag_lengths[0] != diag_lengths[1]:
            raise NotASquare("Diagonals have different length,"
                             "so it isn't a Square")
