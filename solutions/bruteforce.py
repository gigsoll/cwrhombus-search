from classes import point, rhombus, square
from itertools import combinations
from typing import Callable, List, Tuple
from solutions.solution_interface import SolutionInterface


class BrutForce(SolutionInterface):
    def solve(self, file: str, area: Tuple[int, int], 
              on_progress_rhomb: Callable[[int, int], None] = lambda i, total: None,
              on_progress_square: Callable[[int, int], None] = lambda i, total: None
              ) -> Tuple[List[square.Square], List[rhombus.Rhombus]]:
        points = point.point_reader(file)
    
        if isinstance(points, str):
            raise ValueError("File does not exist")
    
        # Find rhombuses with progress reporting
        rhombuses = self.find_rhombuses(points, on_progress_rhomb)
    
        # Find squares with progress reporting
        squares, remaining_rhombs = self.split_into_squares(rhombuses, on_progress_square)
    
        return squares, remaining_rhombs


    def find_rhombuses(self, points: List[point.Point], on_progress: Callable[[int, int], None]) -> List[rhombus.Rhombus]:
        point_combos = list(combinations(points, 4))
        rhombs = []

        total_combos = len(point_combos)
        for i, combo in enumerate(point_combos):
            try:
                rhombs.append(rhombus.Rhombus(*combo))
            except rhombus.NotARhombus:
                pass
            on_progress(i + 1, total_combos)

        return rhombs

    def split_into_squares(self, rhombuses: List[rhombus.Rhombus], on_progress: Callable[[int, int], None]) -> Tuple[List[square.Square], List[rhombus.Rhombus]]:
        squares = []
        remaining_rhombs = []
        used_points = set()

        for rhomb in rhombuses:
            rhomb_points = {rhomb.point1, rhomb.point2, rhomb.point3, rhomb.point4}

            if used_points.isdisjoint(rhomb_points):
                try:
                    squares.append(square.Square(rhomb.point1, rhomb.point2, rhomb.point3, rhomb.point4))
                    used_points.update(rhomb_points)
                except square.NotASquare:
                    remaining_rhombs.append(rhomb)
                    used_points.update(rhomb_points)

        return squares, remaining_rhombs

    def calc_perp_vectors(self, side: Tuple, x: float, y: float, 
                          is_positive: bool, bound: Tuple[Tuple[int, int], Tuple[int, int]]) -> set:
        raise NotImplementedError("BrutForce does not implement calc_perp_vectors")
