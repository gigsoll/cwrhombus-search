from abc import ABC, abstractmethod
from typing import Callable, List, Tuple
from classes.square import Square
from classes.rhombus import Rhombus
from classes.point import Point


class SolutionInterface(ABC):

    @abstractmethod
    def solve(self, data: List[Point], area: Tuple[int, int], 
              on_progress: Callable[[int, int], None]) -> Tuple[List[Square], List[Rhombus]]:
        """Main solve method to be implemented"""
        pass

    @abstractmethod
    def find_rhombuses(self, points: List, on_progress: Callable[[int, int], None]) -> List[Rhombus]:
        """Method to find all rhombuses from a set of points"""
        pass

    @abstractmethod
    def split_into_squares(self, rhombuses: List[Rhombus], 
                           on_progress: Callable[[int, int], None]) -> Tuple[List[Square], List[Rhombus]]:
        """Method to separate squares from rhombuses"""
        pass

    @abstractmethod
    def calc_perp_vectors(self, side: Tuple, x: float, y: float, 
                          is_positive: bool, bound: Tuple[Tuple[int, int], Tuple[int, int]]) -> set:
        """Calculate perpendicular vectors from a given side"""
        pass
