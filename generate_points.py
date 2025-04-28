from classes.point import point_writer, Point
import random


def generate_points(bounds: tuple[int, int], n: int, file: str) -> None:
    """
    Generate specified number of points based on bounds and write it to file

    :param bounds: min and max value of x or y coordinates
    :param n: number of points to generate
    :param file: name of the file in current directory to save to
    """
    point_set: set[Point] = set()
    while len(point_set) < n:
        point_set.add(Point(
            random.randint(*bounds),
            random.randint(*bounds)))

    point_writer(file, list(point_set))


if __name__ == "__main__":
    generate_points((0, 100), 50, "dots.json")
