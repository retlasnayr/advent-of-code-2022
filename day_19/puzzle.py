from utils import read_in_file, print_output, draw_grid
MATERIALS = [
    "ore",
    "clay",
    "obsidian"
    "geode"
]


class Me:
    def __init__(self):
        self.robots = [Robot("ore")]
        self.inventory = {mat: 0 for mat in MATERIALS}

class Robot:
    def __init__(self, robo_type, ):
        if robo_type not in MATERIALS:
            raise ValueError(f"Invalid robot type {robo_type} provided")
        self.type = robo_type
        self.ingredients =



class Blueprint:
    def __init__(self, line):
        self.robots = parse_blueprint(line)


def parse_blueprint(line):
    line = line.split(". ")
    returns = {}
    for part in line:
        part = part.split("robot")[0]
        robot_type = parse_item(part[0])[0]
        robot_cost = parse_item(part[1])
        returns[robot_type] = robot_cost
    return returns

def parse_item(string):
    if "and" in string:
        pieces = string.split(" and ")
        return [parse_item(piece) for piece in pieces]
    pieces = string.split(" ")
    robot = None
    number = None
    for piece in pieces:
        if piece in MATERIALS:
            robot = piece
        try:
            number = int(piece)
        except ValueError:
            pass
        return [robot, number]


def part_1(file_path):
    return ""


def part_2(file_path):
    return ""


if __name__ == "__main__":
    print_output(part_1, part_2)

