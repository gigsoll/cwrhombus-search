from itertools import combinations
from classes.point import point_reader, Point
from classes.rhombus import Rhombus
from classes.square import Square, NotASquare
import math


def smort(file: str, area: tuple[int, int]) -> list:
    points = point_reader("dots.json")
    combos = combinations(points, 2)
    sorted_cobos = sorted(combos, key=lambda c: Rhombus.calculate_distance(*c))
    combos = list(sorted_cobos)  # sort lines start from shortest
    used_points = set()
    points_set = set(points)
    rhomuses = list()
    boundary = (area, area)  # search area, must be changed

    for combo in combos:
        if combo[0] in used_points or combo[1] in used_points:
            continue  # scip after all

        middle_x = (combo[0].x + combo[1].x) / 2
        middle_y = (combo[0].y + combo[1].y) / 2

        p1, p2 = combo

        middle_point = Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)
        vec1 = calc_perp_vectors(combo, middle_x, middle_y, True, boundary)
        vec2 = calc_perp_vectors(combo, middle_x, middle_y, False, boundary)

        points1 = points_set.intersection(vec1)
        points2 = points_set.intersection(vec2)

        # Get the distances from the middle point
        dist1 = {(pt.x - middle_point.x)**2 + (pt.y - middle_point.y)**2: pt for pt in points1}  # noqa
        dist2 = {(pt.x - middle_point.x)**2 + (pt.y - middle_point.y)**2: pt for pt in points2}  # noqa

        if points1 and points2:
            dist_vec_1_cleaned = set(dist1)
            dist_vec_1_cleaned.discard(0.0)
            dist_vec_2_cleaned = set(dist2)
            dist_vec_2_cleaned.discard(0.0)

            if dist_vec_1_cleaned and dist_vec_2_cleaned\
                    and dist_vec_1_cleaned.intersection(dist_vec_2_cleaned):
                # Find common distance
                common_distance = dist_vec_1_cleaned.\
                    intersection(dist_vec_2_cleaned).pop()
                points_1_dict = dict(zip(dist1, points1))
                points_2_dict = dict(zip(dist2, points2))

                # get the points corresponding to the common distance
                point1 = points_1_dict[common_distance]
                point2 = points_2_dict[common_distance]

                if point1 in used_points or point2 in used_points:
                    continue

                rhomuses.append(Rhombus(combo[0], combo[1], point1, point2))

                # save used points
                used_points.update([combo[0], combo[1], point1, point2])

    squares = []
    remaining_rhombs = []
    for rhomb in rhomuses:
        try:
            s = Square(rhomb.point1, rhomb.point2,
                       rhomb.point3, rhomb.point4)
            squares.append(s)
        except NotASquare:
            remaining_rhombs.append(rhomb)

    return squares, remaining_rhombs


def calc_perp_vectors(side: tuple[Point, Point],
                      x: float, y: float,
                      is_positive: bool,
                      bound: tuple[tuple[int, int], tuple[int, int]]) -> set[Point]:  # noqa
    vec_side = side[1].x - side[0].x, side[1].y - side[0].y
    perp = (vec_side[1], -vec_side[0]) if is_positive else (-vec_side[1],
                                                            vec_side[0])

    # find unit vector for future
    perp_mag = math.sqrt(perp[0]**2 + perp[1]**2)
    perp_unit = (perp[0] / perp_mag, perp[1] / perp_mag)

    points = []

    # build using unit vector
    current_x, current_y = x, y

    while (bound[0][0] <= current_x <= bound[0][1]) and\
          (bound[1][0] <= current_y <= bound[1][1]):
        points.append(Point(round(current_x, 2), round(current_y, 2)))
        current_x += perp_unit[0] * 0.5  # step 0.5 to satisfy task
        current_y += perp_unit[1] * 0.5  # step 0.5 to satisfy task

    return set(points)
