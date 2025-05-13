from dataclasses import dataclass, asdict
import json
import os


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


def point_reader(file: str) -> list[Point] | str:
    read_data = []
    result = []
    try:
        with open(os.path.join(os.getcwd(), file), "r") as json_points:
            read_data = json.load(json_points)
    except FileNotFoundError:
        return "File not found"
    for point in read_data:
        result.append(Point(**point))
    return result


def point_writer(file: str, data: list[Point]) -> None | str:
    try:
        with open(os.path.join(os.getcwd(), file), "w") as write_to:
            dict_data = [asdict(point) for point in data]
            write_to.write(json.dumps(dict_data, indent=4))
    except FileNotFoundError:
        return "File not found, make sure you correctly specified the path"
    return None
