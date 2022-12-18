from utils import read_in_file, print_output, draw_grid, Pair


class PieceGenerator:
    def __init__(self):
        self.pieces = [
            {Pair(0, 0), Pair(1, 0), Pair(2, 0), Pair(3, 0)},
            {Pair(1, 0), Pair(0, 1), Pair(1, 1), Pair(2, 1), Pair(1, 2)},
            {Pair(0, 0), Pair(1, 0), Pair(2, 0), Pair(2, 1), Pair(2, 2)},
            {Pair(0, 0), Pair(0, 1), Pair(0, 2), Pair(0, 3)},
            {Pair(0, 0), Pair(1, 0), Pair(0, 1), Pair(1, 1)}
        ]
        self.last_index = -1

    def next(self):
        self.last_index += 1
        return self.pieces[self.last_index % len(self.pieces)]


class Jets:
    def __init__(self, jets):
        self.jets = [{"<": Pair(-1, 0), ">": Pair(1, 0)}[char] for char in jets]
        self.last_index = -1

    def next(self):
        self.last_index += 1
        return self.jets[self.last_index % len(self.jets)]


class Chamber:
    def __init__(self, jets):
        self.width = 7
        self.walls = (0, self.width + 2)
        self.stationary_rocks = {Pair(x + 1, 0) for x in range(self.width)}
        self.jets = Jets(jets)
        self.rocks = PieceGenerator()
        self.tops = [0 for _ in range(self.width)]
        self.states = {}

    def spawn_position(self):
        max_height = max(piece.y for piece in self.stationary_rocks)
        return Pair(2, max_height + 4)

    def simulate_rock(self):
        spawn = self.spawn_position()
        rock = {spawn + piece for piece in self.rocks.next()}
        while True:
            # print(self.draw_chamber(rock))
            jet = self.jets.next()
            test_position = {jet + piece for piece in rock}
            if not any(piece.x == -1 or piece.x == self.width for piece in test_position):
                if not any(piece in self.stationary_rocks for piece in test_position):
                    rock = test_position
            test_position = {Pair(0, -1) + piece for piece in rock}
            # print(self.draw_chamber(rock))
            if any(piece in self.stationary_rocks or piece.y == 0 for piece in test_position):
                self.stationary_rocks.update(rock)
                break
            rock = test_position
            # print(self.draw_chamber(rock))
            pass

    def simulate_rocks(self, number):
        height = 0
        for iter in range(number):
            if (self.jets.last_index, self.rocks.last_index) not in self.states:
                self.states[(self.jets.last_index, self.rocks.last_index)] = max(piece.y for piece in self.stationary_rocks)
                self.simulate_rock()
            else:
                height = (number // iter) * (self.states[(self.jets.last_index, self.rocks.last_index)] - 1)
                for it in range(number % iter):
                    self.simulate_rock()
        return height + max(piece.y for piece in self.stationary_rocks)





    def draw_chamber(self, new_rock=None):
        height = max(self.tops) + 6
        grid = [["|", ".", ".", ".", ".", ".", ".", ".", "|"] for y in range(height)]
        grid.append(["+", "-", "-", "-", "-", "-", "-", "-", "+"])
        for rock in self.stationary_rocks:
            grid[height - rock.y][1 + rock.x] = "#"
        for x, y in enumerate(self.tops):
            grid[height - y][1 + x] = "#"
        if new_rock is not None:
            for rock in new_rock:
                grid[height - rock.y][1 + rock.x] = "@"
        return draw_grid(grid)


def part_1(file_path):
    read_in = read_in_file(file_path)
    chamber = Chamber(read_in[0])
    return chamber.simulate_rocks(2022)
    # return max(rock.y for rock in chamber.stationary_rocks)



def part_2(file_path):
    read_in = read_in_file(file_path)
    chamber = Chamber(read_in[0])
    return chamber.simulate_rocks(int(1e12))

    # return max(rock.y for rock in chamber.stationary_rocks)



if __name__ == "__main__":
    print_output(part_1, part_2)

