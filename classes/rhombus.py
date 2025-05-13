from dataclasses import dataclass

from .exceptions import NotARhombus
from .point import Point
from .quadrilateral import Quadrilateral


@dataclass
class Rhombus(Quadrilateral):
    def __post_init__(self):
        side_lengths = self.calculate_sides()
        if len(set(side_lengths)) > 1:
            raise NotARhombus("Sides aren't equal, so it is not a rhombus.")

    def __repr__(self, emoji: str = "♦️") -> str:
        return f"{emoji} {self.point1}, {self.point2}, {self.point3}, {self.point4}"

    def calculate_area(self):
        diag1, diag2 = self.calculate_diagonals()
        return (diag1 * diag2) / 2


if __name__ == "__main__":
    r = Rhombus(
        Point(0, 0),
        Point(1, 0),
        Point(0, 1),
        Point(1, 10)
        )
    print(r.calculate_sides())
