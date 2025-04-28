from dataclasses import dataclass
from .quadrilateral import Quadrilateral
from .exceptions import NotARhombus
from .point import Point


@dataclass
class Rhombus(Quadrilateral):
    def __post_init__(self):
        side_lengths = self.calculate_sides()
        if len(set(side_lengths)) > 1:
            raise NotARhombus("Sides aren't equal, so it is not a rhombus.")


if __name__ == "__main__":
    r = Rhombus(
        Point(0, 0),
        Point(1, 0),
        Point(0, 1),
        Point(1, 10)
        )
    print(r.calculate_sides())
