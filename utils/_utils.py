

def read_in_file(file_path):
    """
    Read in text file at file path, then split to a list on the newline (\n) character
    :param file_path: Local file path to read in
    :return: List of strings, each element is one line from the input file.
    """
    with open(file_path) as f:
        input_lines = f.read()
        input_lines = input_lines.split("\n")
    return input_lines

def print_output(part_1, part_2):
    print("Part 1")
    print("Example:", part_1("example.txt"))
    print("Real   :", part_1("input.txt"))
    print("\nPart 2")
    print("Example:", part_2("example.txt"))
    print("Real   :", part_2("input.txt"))


def draw_grid(grid):
    return "\n".join([" ".join(str(x) for x in row) for row in grid])


class Pair(list):

    def __init__(self, x, y):
        super().__init__((x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __add__(self, other):
        return Pair(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        return Pair(self[0] - other[0], self[1] - other[1])

    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1]

    def __hash__(self):
        return tuple(self).__hash__()

    def is_adjacent_to(self, other):
        diff = self - other
        return diff[0] in (-1, 0, 1) and diff[1] in (-1, 0, 1)


DIRECTION_VECTORS = {
    "R": Pair(1, 0),
    "L": Pair(-1, 0),
    "U": Pair(0, 1),
    "D": Pair(0, -1)
}
