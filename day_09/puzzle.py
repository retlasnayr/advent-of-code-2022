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
    knot_positions = {i: set(Pair(0, 0)) for i in range(10)}

    # Update head position:
    for inst in insts:
        for step in range(int(inst[1])):
            rope[0] = get_new_head_pos(rope[0], inst)

            for i in range(9):
                rope[i], rope[i+1], knot_positions[i+1] = simulate_step(rope[i], rope[i+1], knot_positions[i+1])

    return {k: len(v) for k, v in knot_positions.items()}


if __name__ == "__main__":
    print_output(part_1, part_2)

