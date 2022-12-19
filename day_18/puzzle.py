from utils import read_in_file, print_output, draw_grid, NTuple

DIRECTIONS = [
    NTuple((-1, 0, 0)),
    NTuple((1, 0, 0)),
    NTuple((0, -1, 0)),
    NTuple((0, 1, 0)),
    NTuple((0, 0, -1)),
    NTuple((0, 0, 1))
]

class LavaCube(NTuple):
    def __init__(self, args, data_type=None):
        super().__init__(args, data_type=data_type)

    @property
    def neighbours(self):
        return [self + direction for direction in DIRECTIONS]

class LavaDroplet:
    def __init__(self, cubes):
        self.cubes = [LavaCube(cube.split(","), data_type=int) for cube in cubes]
        self.max = LavaCube((
            max(cube.x for cube in self.cubes),
            max(cube.y for cube in self.cubes),
            max(cube.z for cube in self.cubes)
        ))
        self.min = LavaCube((
            min(cube.x for cube in self.cubes),
            min(cube.y for cube in self.cubes),
            min(cube.z for cube in self.cubes)
        ))

    def count_neighbours(self, cube: LavaCube):
        num = 0
        for adj_location in cube.neighbours:
            if adj_location in self.cubes:
                num += 1
        return num

    def calc_surface_area(self):
        total_sa = 0
        for cube in self.cubes:
            total_sa += 6 - self.count_neighbours(cube)
        return total_sa

    def calc_external_sa(self):
        total_sa = 0
        for cube in self.cubes:
            if self.cube_on_edge(cube):
                total_sa += 6 - self.count_neighbours(cube)
        return total_sa

    def cube_on_edge(self, cube):
        if cube.x >= self.max.x or cube.x <= self.min.x or cube.y >= self.max.y or cube.y <= self.min.y or cube.z >= self.max.z or cube.z <= self.min.z:
            return True
        return False


def part_1(file_path):
    lines = read_in_file(file_path)
    drop = LavaDroplet(lines)
    return drop.calc_surface_area()


def part_2(file_path):
    lines = read_in_file(file_path)
    drop = LavaDroplet(lines)
    return drop.calc_external_sa()


if __name__ == "__main__":
    print(part_2("example.txt"))
    # print_output(part_1, part_2)

