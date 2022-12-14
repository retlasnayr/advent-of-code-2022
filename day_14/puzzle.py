from utils import read_in_file, print_output, draw_grid, Pair

class Grid:
    def __init__(self, rocks, source):
        self.rocks = rocks
        self.source = source
        self.moving_sand = None
        self.sand = []

        self.min_x = min(min(point.x for point in rocks), source.x)
        self.max_x = max(max(point.x for point in rocks), source.x)
        self.min_y = min(min(point.y for point in rocks), source.y)
        self.max_y = max(max(point.y for point in rocks), source.y)

        self.grid = self.blank_grid()
        self.draw_cave()

    def blank_grid(self):
        return [["." for x in range(self.min_x - 1, self.max_x + 2)] for y in range(self.min_y - 1, self.max_y + 2)]
    def set_grid_val(self, x, y, val):
        self.grid[y - self.min_y + 1][x - self.min_x + 1] = val

    def get_grid_val(self, pair):
        return self.grid[pair.y - self.min_y + 1][pair.x - self.min_x + 1]

    def draw_cave(self):
        # self.grid = [["." for x in range(self.min_x - 1, self.max_x + 2)] for y in range(self.min_y - 1, self.max_y + 2)]
        self.set_grid_val(self.source.x, self.source.y, "+")

        for rock in self.rocks:
            self.set_grid_val(rock.x, rock.y, "#")
        for sand in self.sand:
            self.set_grid_val(sand.x, sand.y, "o")
        # if self.moving_sand is not None:
        #     self.set_grid_val(self.moving_sand.x, self.moving_sand.y, "s")

    def output_cave(self):
        return draw_grid(self.grid)

    def timestep(self):
        if self.moving_sand is None:
            self.moving_sand = self.source
        if self.move_sand():
            return len(self.sand)
        self.draw_cave()

    def move_sand(self):
        if self.moving_sand.y == self.max_y:
            return True
        if self.get_grid_val(new_pos := self.moving_sand + Pair(0, 1)) == ".":
            self.moving_sand = new_pos
        elif self.get_grid_val(new_pos := self.moving_sand + Pair(-1, 1)) == ".":
            self.moving_sand = new_pos
        elif self.get_grid_val(new_pos := self.moving_sand + Pair(1, 1)) == ".":
            self.moving_sand = new_pos
        else:

            self.sand.append(self.moving_sand)
            if self.moving_sand == self.source:
                return True
            self.moving_sand = None



class Grid_p2(Grid):
    def __init__(self, rocks, source):
        super().__init__(rocks, source)
        self.min_x = min(self.min_x, self.source.x - (self.source.y + self.max_y) - 5)
        self.max_x = max(self.max_x, self.source.x + (self.source.y + self.max_y) + 5)
        self.max_y = self.max_y + 2
        for i in range(self.min_x, self.max_x + 1):
            self.rocks.append(Pair(i, self.max_y))
        self.grid = self.blank_grid()
        self.draw_cave()



def interpolate_points(p1: Pair, p2: Pair):
    if p1.x == p2.x:
        min_y = min(p1.y, p2.y)
        max_y = max(p1.y, p2.y)
        return [Pair(p1.x, y) for y in range(min_y, max_y + 1)]
    if p1.y == p2.y:
        min_x = min(p1.x, p2.x)
        max_x = max(p1.x, p2.x)
        return [Pair(x, p1.y) for x in range(min_x, max_x + 1)]
    raise ValueError(f"Point {p1} and {p2} are not vertically or horizontally aligned")


def part_1(file_path):
    lines = read_in_file(file_path)
    clean_lines = [[Pair(int(item.split(",")[0]), int(item.split(",")[1])) for item in line.split(" -> ")] for line in lines]
    rocks = []
    for line in clean_lines:
        for index, _ in enumerate(line[:-1]):
            rocks.extend(interpolate_points(line[index], line[index+1]))
    grid = Grid(rocks, Pair(500, 0))
    print(grid.output_cave())
    while True:
        sand = grid.timestep()
        if sand is not None:
            break
    grid.draw_cave()
    print(grid.output_cave())
    return sand


def part_2(file_path):
    lines = read_in_file(file_path)
    clean_lines = [[Pair(int(item.split(",")[0]), int(item.split(",")[1])) for item in line.split(" -> ")] for line in
                   lines]
    rocks = []
    for line in clean_lines:
        for index, _ in enumerate(line[:-1]):
            rocks.extend(interpolate_points(line[index], line[index + 1]))
    grid = Grid_p2(rocks, Pair(500, 0))
    while True:
        sand = grid.timestep()
        if sand is not None:
            break
    grid.draw_cave()
    print(grid.output_cave())
    return(sand)


if __name__ == "__main__":
    print_output(part_1, part_2)


