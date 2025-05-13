import math
from itertools import combinations
from typing import Callable, List, Set, Tuple

from classes import point, rhombus, square
from solutions.solution_interface import SolutionInterface


class BrutForce(SolutionInterface):
    def __init__(self):
        self._rhombus_points_cache = {}

    def solve(self, data: List[point.Point], area: Tuple[int, int],
              on_progress: Callable[[int, int], None] = lambda i, total: None
              ) -> Tuple[List[square.Square], List[rhombus.Rhombus]]:
        points = data

        if isinstance(points, str):
            raise ValueError("File does not exist")

        if len(points) < 4:
            return [], []

        # Find rhombuses with progress reporting
        rhombuses = self.find_rhombuses(points, on_progress)

        # Find squares with progress reporting
        squares, remaining_rhombs = self.split_into_squares(
            rhombuses, on_progress
        )

        return squares, remaining_rhombs

    def find_rhombuses(self, points: List[point.Point],
                      on_progress: Callable[[int, int], None]
                      ) -> List[rhombus.Rhombus]:
        # Direct calculation without creating list
        total_combos = math.comb(len(points), 4)
        # Update every 1% or every item if small
        update_threshold = max(1, total_combos // 100)
        rhombs = []

        for i, combo in enumerate(combinations(points, 4)):
            try:
                rhombs.append(rhombus.Rhombus(*combo))
            except rhombus.NotARhombus:
                pass
            if i % update_threshold == 0:
                on_progress(i + 1, total_combos)
        
        on_progress(total_combos, total_combos)
        return rhombs

    def split_into_squares(self, rhombuses: List[rhombus.Rhombus],
                          on_progress: Callable[[int, int], None]
                          ) -> Tuple[List[square.Square], List[rhombus.Rhombus]]:
        squares = []
        remaining_rhombs = []
        used_points = set()
        total_rhombs = len(rhombuses)
        update_threshold = max(1, total_rhombs // 100)

        for i, rhomb in enumerate(rhombuses):
            # Use cached points if available
            if id(rhomb) not in self._rhombus_points_cache:
                self._rhombus_points_cache[id(rhomb)] = {
                    rhomb.point1, rhomb.point2,
                    rhomb.point3, rhomb.point4
                }
            rhomb_points = self._rhombus_points_cache[id(rhomb)]

            if used_points.isdisjoint(rhomb_points):
                try:
                    squares.append(square.Square(
                        rhomb.point1, rhomb.point2,
                        rhomb.point3, rhomb.point4
                    ))
                except square.NotASquare:
                    remaining_rhombs.append(rhomb)
                used_points.update(rhomb_points)

            if i % update_threshold == 0:
                on_progress(i + 1, total_rhombs)

        on_progress(total_rhombs, total_rhombs)
        return squares, remaining_rhombs

    def calc_perp_vectors(self, side: Tuple, x: float, y: float,
                         is_positive: bool,
                         bound: Tuple[Tuple[int, int], Tuple[int, int]]
                         ) -> set:
        raise NotImplementedError(
            "BrutForce does not implement calc_perp_vectors"
        )
