from utils import read_in_file, print_output


class Pair(list):

    def __init__(self, x, y):
        super().__init__((x, y))

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


def part_1(file_path):
    instructions = read_in_file(file_path)
    insts = [x.split(" ") for x in instructions]
    head_pos = Pair(0, 0)
    tail_pos = Pair(0, 0)
    seen_positions = {tail_pos}
    for inst in insts:
        head_pos, tail_pos, seen_positions = simulate_steps(head_pos, tail_pos, inst, seen_positions)
    return len(seen_positions)


def simulate_steps(head_pos, tail_pos, inst, seen_positions):
    for step in range(int(inst[1])):
        new_head_pos = get_new_head_pos(head_pos, inst)
        head_pos, tail_pos, seen_positions = simulate_step(new_head_pos, tail_pos, seen_positions)
    return head_pos, tail_pos, seen_positions


def get_new_head_pos(head_pos, inst):
    return head_pos + DIRECTION_VECTORS[inst[0]]


def simulate_step(new_head_pos, tail_pos, seen_positions):
    if not tail_pos.is_adjacent_to(new_head_pos):
        tail_pos = get_new_tail_pos(new_head_pos, tail_pos)
        seen_positions.add(tail_pos)
    return new_head_pos, tail_pos, seen_positions


def get_new_tail_pos(head_pos, tail_pos):
    difference = head_pos - tail_pos
    movement_vector = Pair(sign(difference[0]), sign(difference[1]))
    tail_pos = tail_pos + movement_vector
    return tail_pos


def sign(x: int):
    if x == 0:
        return x
    return x/abs(x)


def part_2(file_path):
    instructions = read_in_file(file_path)
    insts = [x.split(" ") for x in instructions]
    rope = {i: Pair(0, 0) for i in range(10)}
    knot_positions = {i: {Pair(0, 0)} for i in range(10)}

    # Update head position:
    for inst in insts:
        for step in range(int(inst[1])):
            rope[0] = get_new_head_pos(rope[0], inst)

            for i in range(9):
                rope[i], rope[i+1], knot_positions[i+1] = simulate_step(rope[i], rope[i+1], knot_positions[i+1])
            # draw_grid(rope)
    plot_path(knot_positions)
    return {k: len(v) for k, v in knot_positions.items()}


def draw_grid(positions):
    min_x = min(pos[0] for pos in positions.values())
    max_x = max(pos[0] for pos in positions.values())
    min_y = min(pos[1] for pos in positions.values())
    max_y = max(pos[1] for pos in positions.values())

    grid = [["-" for x in range(int(max_x - min_x + 1))] for y in range(int(max_y - min_y + 1))]

    for name, pos in positions.items():
        grid_item = grid[int(pos[1] - min_y)][int(pos[0] - min_x)]
        if grid_item == "-":
            grid[int(pos[1] - min_y)][int(pos[0] - min_x)] = name
    print("\n".join([" ".join(str(x) for x in row) for row in grid]))
    print("\n")


def plot_path(positions):
    positions = positions[max(positions.keys())]
    min_x = int(min(pos[0] for pos in positions))
    max_x = int(max(pos[0] for pos in positions))
    min_y = int(min(pos[1] for pos in positions))
    max_y = int(max(pos[1] for pos in positions))

    grid = [["-" for x in range(int(max_x - min_x + 1))] for y in range(int(max_y - min_y + 1))]

    for pos in positions:
        grid[int(pos[1] - min_y)][int(pos[0] - min_x)] = "#"
    grid[-min_y][-min_x] = "s"
    print_grid = "\n".join([" ".join(str(x) for x in row) for row in grid][::-1])
    print(print_grid)
    with open("grid.txt", "w") as f:
        f.write(print_grid)
    print("\n")

if __name__ == "__main__":
    print_output(part_1, part_2)

