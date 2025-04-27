from dataclasses import dataclass, field
from point import Point
from linkedList import CircularLinkedList
import math


@dataclass
class Quadrilateral:
    point1: Point
    point2: Point
    point3: Point
    point4: Point

    def order_points(self) -> tuple[Point, ...]:
        """
        Calculates order in which to create not overlapping polygon
        """
        points = self.point1, self.point2, self.point3, self.point4

        # Calculate centroids
        centroid_x = sum([point.x for point in points]) / 4
        centroid_y = sum([point.y for point in points]) / 4

        distances = dict.fromkeys([0, 1, 2, 3])
        for i, point in enumerate(points):
            distances[i] = math.atan2(
                point.y - centroid_y,
                point.x - centroid_x)
        distances = self.sort_dict(distances)

        return tuple(points[i] for i in distances.keys())

    def create_circular_linked_list(self) -> CircularLinkedList:
        """
        Converts calculated previously tuple of points into CircularLinkedList
        """
        ordered_points = self.order_points()
        points_cll = CircularLinkedList()
        for point in ordered_points:
            points_cll.addAtEnd(point)
        return points_cll

    def calculate_diagonals(self) -> tuple[float, float]:
        """
        Calculate length of diagonals
        """
        points: CircularLinkedList = self.create_circular_linked_list()
        diag_anchor1, diag_anchor2 = points.traverse()[0], points.traverse()[1]
        diag1 = (diag_anchor1, points.traverseWithStep(2, 1, diag_anchor1)[0])
        diag2 = (diag_anchor2, points.traverseWithStep(2, 1, diag_anchor2)[0])

        # It was ugly and I was not proud of it, now it is pretty
        len_diag1: float = self.calculate_distance(*diag1)
        len_diag2: float = self.calculate_distance(*diag2)
        return len_diag1, len_diag2

    def calculate_sides(self) -> tuple[float, ...]:
        """
        Calculate length of each side
        """
        vertices = self.create_circular_linked_list()
        current_vert = vertices.traverse()[0]
        result: list[float] = []
        for i in range(4):
            next_vert = vertices.traverseWithStep(1, 1, current_vert)[0]
            result.append(self.calculate_distance(current_vert, next_vert))
            current_vert = next_vert

        return tuple(result)

    @staticmethod
    def sort_dict(dictionary: dict) -> dict:
        """
        Sort dict by values, saving order of keys
        """
        return dict(sorted(dictionary.items(), key=lambda item: item[1]))

    @staticmethod
    def calculate_distance(point1: Point, point2: Point) -> float:
        """
        Gets two points and returns distance between them
        """
        return round(math.sqrt(
            math.sqrt(math.pow(point2.x - point1.x, 2)) +
            math.sqrt(math.pow(point2.y - point1.y, 2))),
            3)


if __name__ == "__main__":
    r = Quadrilateral(
        Point(0, 0),
        Point(1, 0),
        Point(0, 1),
        Point(1, 1)
        )
    print(r.calculate_sides())
