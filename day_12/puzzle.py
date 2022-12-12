from utils import read_in_file, print_output, draw_grid, Pair, DIRECTION_VECTORS

OPPOSITE = {
    "U": "D",
    "D": "U",
    "L": "R",
    "R": "L"
}

def compare_heights(current, target):
    return ord(target) - ord(current) <= 1


class Grid:
    def __init__(self, lines):
        self.height = None
        self.width = None
        self.data = None
        self.start_location = None
        self.end_location = None
        self.from_lines(lines)
        self.find_start_end()
        self.routes = []

    def from_lines(self, lines):
        self.data = [[x for x in line] for line in lines]
        self.width = len(lines[0])
        self.height = len(lines)

    def row(self, n):
        return self.data[n]

    def column(self, n):
        return [x[n] for x in self.data]

    def cell_value(self, coords: Pair):
        if coords[0] < 0 or coords[0] >= self.width or coords[1] < 0 or coords[1] >= self.height:
            raise ValueError("Cell index out of grid")
        return self.data[coords[1]][coords[0]]

    def get_adjacent(self, direction, current_location):
        loc = current_location + DIRECTION_VECTORS[direction]
        return loc, self.cell_value(loc)

    def find_start_end(self):
        for row_index, row in enumerate(self.data):
            for col_index, col in enumerate(row):
                if col == "S":
                    self.start_location = Pair(col_index, row_index)
                    self.data[row_index][col_index] = "a"
                    continue
                if col == "E":
                    self.end_location = Pair(col_index, row_index)
                    self.data[row_index][col_index] = "z"

    def find_route(self, route_so_far=None):
        if route_so_far is None:
            for direction in ("U", "D", "L", "R"):
                return self.find_route([self.start_location, self.start_location + DIRECTION_VECTORS[direction]])
        for direction in ("U", "D", "L", "R"):
            try:
                test_target = self.get_adjacent(direction, route_so_far[-1])
                # if test_target[0] == self.end_location:
                #     route_so_far.append(self.end_location)
                #     return route_so_far
            except ValueError:
                continue
            if test_target[0] in route_so_far:
                continue
            if compare_heights(self.cell_value(route_so_far[-1]), test_target[1]):
                new_route = route_so_far + [Pair(*test_target[0])]
                if new_route[-1] == self.end_location:
                    # if route_so_far not in self.routes:
                    self.routes.append(new_route)
                    continue
                else:
                    self.find_route(route_so_far=new_route)
                    continue





    def print_route(self, route):
        grid_pic = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for num, pair in enumerate(route[:-1]):
            direction = {Pair(0, 1): "v", Pair(1, 0): ">", Pair(-1, 0): "<", Pair(0, -1): "^"}[route[num+1]-pair]
            grid_pic[pair[1]][pair[0]] = direction
        return draw_grid(grid_pic)




def part_1(file_path):
    lines = read_in_file(file_path)
    grid = Grid(lines)
    grid.find_route()
    print(draw_grid(grid.data))
    print("\n")
    print(grid.print_route(grid.routes[0]))
    print(grid.routes)
    return(min([len(x) for x in grid.routes]) -1)


def part_2(file_path):
    return ""


if __name__ == "__main__":
    print_output(part_1, part_2)

