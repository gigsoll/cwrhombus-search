from itertools import combinations
from classes.point import Point, point_reader
from classes.rhombus import Rhombus, NotARhombus
from classes.square import Square, NotASquare
from solutions.solution_interface import SolutionInterface
import math
from typing import Callable, List, Tuple, Set


class Smart(SolutionInterface):

    def solve(self, data: List[Point], area: Tuple[int, int], 
              on_progress: Callable[[int, int], None] = lambda i, total: None
              ) -> Tuple[List[Square], List[Rhombus]]:
        points = data
        rhombuses = self.find_rhombuses(points, area, on_progress)
        squares, remaining_rhombs = self.split_into_squares(rhombuses, on_progress)

        return squares, remaining_rhombs

    def find_rhombuses(self, points: List[Point], 
                       area: Tuple[int, int], 
                       on_progress: Callable[[int, int], None]) -> List[Rhombus]:
        combos = list(combinations(points, 2))
        points_set = set(points)
        used_points = set()
        rhombuses = []
        boundary = (area, area)
        total = len(combos)

        for i, (p1, p2) in enumerate(combos):
            if p1 in used_points or p2 in used_points:
                on_progress(i + 1, total)
                continue

            # Midpoint calculation
            middle_x = (p1.x + p2.x) / 2
            middle_y = (p1.y + p2.y) / 2
            middle_point = Point(middle_x, middle_y)

            # Calculate perpendicular vectors
            vec1 = self.calc_perp_vectors((p1, p2), middle_x, middle_y, True, boundary)
            vec2 = self.calc_perp_vectors((p1, p2), middle_x, middle_y, False, boundary)

            # Optimize by intersecting with the original point set directly
            points1 = points_set & vec1
            points2 = points_set & vec2

            if not points1 or not points2:
                on_progress(i + 1, total)
                continue

            # Calculate distances to the middle point and remove 0 distances
            dist1 = {(pt.x - middle_point.x) ** 2 + (pt.y - middle_point.y) ** 2: pt for pt in points1}
            dist2 = {(pt.x - middle_point.x) ** 2 + (pt.y - middle_point.y) ** 2: pt for pt in points2}

            # Get the common distances and filter out the origin (0,0)
            common_distances = dist1.keys() & dist2.keys()
            common_distances.discard(0.0)

            if common_distances:
                common_distance = min(common_distances)  # Pick the smallest one
                point1 = dist1[common_distance]
                point2 = dist2[common_distance]

                if point1 in used_points or point2 in used_points:
                    on_progress(i + 1, total)
                    continue

                try:
                    rhombuses.append(Rhombus(p1, p2, point1, point2))
                    used_points.update({p1, p2, point1, point2})
                except NotARhombus:
                    continue

            on_progress(i + 1, total)

        return rhombuses

    def split_into_squares(self, rhombuses: List[Rhombus], 
                           on_progress: Callable[[int, int], None]) -> Tuple[List[Square], List[Rhombus]]:
        """
        Efficiently splits rhombuses into squares if possible.
        """
        squares = []
        remaining_rhombs = []

        for rhomb in rhombuses:
            try:
                squares.append(Square(rhomb.point1, rhomb.point2, rhomb.point3, rhomb.point4))
            except NotASquare:
                remaining_rhombs.append(rhomb)

        return squares, remaining_rhombs

    def calc_perp_vectors(self, side: Tuple[Point, Point], 
                          x: float, y: float, 
                          is_positive: bool, 
                          bound: Tuple[Tuple[int, int], Tuple[int, int]]) -> Set[Point]:
        vec_side = side[1].x - side[0].x, side[1].y - side[0].y
        perp = (vec_side[1], -vec_side[0]) if is_positive else (-vec_side[1], vec_side[0])

        perp_mag = math.sqrt(perp[0] ** 2 + perp[1] ** 2)
        perp_unit = (perp[0] / perp_mag, perp[1] / perp_mag)

        points = set()
        current_x, current_y = x, y
        step = 0.5

        max_steps = 1000
        for _ in range(max_steps):
            if not (bound[0][0] <= current_x <= bound[0][1]) or not (bound[1][0] <= current_y <= bound[1][1]):
                break
            points.add(Point(round(current_x, 2), round(current_y, 2)))
            current_x += perp_unit[0] * step
            current_y += perp_unit[1] * step

        return points
