from classes import point, rhombus, square
from itertools import combinations


def brutforce(file: str) -> tuple[list[square.Square], list[rhombus.Rhombus]]:
    points: list[point.Point] | str = point.point_reader(file)

    if isinstance(points, str):
        raise ValueError("You entered not existing file")

    # Generate all combinations of 4 points
    point_combos = combinations(points, 4)
    rhombs: list[rhombus.Rhombus] = []

    for combo in point_combos:
        try:
            rhombs.append(rhombus.Rhombus(*combo))
        except rhombus.NotARhombus:
            pass

    areas = [r.calculate_area() for r in rhombs]
    pairs = list(zip(areas, rhombs))
    rhombs = [pair[1] for pair in sorted(pairs, key=lambda x: x[0])]

    squares: list[square.Square] = []
    remaining_rhombs: list[rhombus.Rhombus] = []
    used_points: set[point.Point] = set()

    for rhomb in rhombs:
        rhomb_points = {rhomb.point1, rhomb.point2, rhomb.point3, rhomb.point4}

        if not used_points.isdisjoint(rhomb_points):
            continue

        try:
            s = square.Square(rhomb.point1, rhomb.point2,
                              rhomb.point3, rhomb.point4)
            squares.append(s)
            used_points.update(rhomb_points)
        except square.NotASquare:
            remaining_rhombs.append(rhomb)
            used_points.update(rhomb_points)

    return squares, remaining_rhombs
