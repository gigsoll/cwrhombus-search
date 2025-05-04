from classes import point, rhombus, square
from itertools import combinations
from typing import Callable


def brutforce(file: str,
              on_progress_rhomb: Callable[[int, int], None] = lambda i, total: None,  # noqa
              on_progress_square: Callable[[int, int], None] = lambda i, total: None  # noqa
              ) -> tuple[list[square.Square], list[rhombus.Rhombus]]:
    points: list[point.Point] | str = point.point_reader(file)

    if isinstance(points, str):
        raise ValueError("File does not exitsts")

    # Generate all combinations of 4 points
    point_combos = list(combinations(points, 4))
    rhombs: list[rhombus.Rhombus] = []

    total_combos = len(point_combos)
    for i, combo in enumerate(point_combos):
        try:
            rhombs.append(rhombus.Rhombus(*combo))
        except rhombus.NotARhombus:
            pass
        on_progress_rhomb(i + 1, total_combos)

    areas = [r.calculate_area() for r in rhombs]
    pairs = list(zip(areas, rhombs))
    rhombs = [pair[1] for pair in sorted(pairs, key=lambda x: x[0])]

    squares: list[square.Square] = []
    remaining_rhombs: list[rhombus.Rhombus] = []
    used_points: set[point.Point] = set()

    total_rhombs = len(rhombs)
    for i, rhomb in enumerate(rhombs):
        rhomb_points = {rhomb.point1, rhomb.point2, rhomb.point3, rhomb.point4}

        if not used_points.isdisjoint(rhomb_points):
            on_progress_square(i + 1, total_rhombs)
            continue

        try:
            s = square.Square(rhomb.point1, rhomb.point2,
                              rhomb.point3, rhomb.point4)
            squares.append(s)
            used_points.update(rhomb_points)
        except square.NotASquare:
            remaining_rhombs.append(rhomb)
            used_points.update(rhomb_points)
        on_progress_square(i + 1, total_rhombs)

    return squares, remaining_rhombs
