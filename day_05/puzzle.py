from utils import read_in_file


def part_1(file_path):
    lines = read_in_file(file_path)
    stacks, instructions = split_input(lines)
    stacks_dict = process_stacks(stacks)
    follow_instructions(stacks_dict, instructions)
    return get_output(stacks_dict)


def split_input(lines):
    split_point = None
    for index, line in enumerate(lines):
        if line.strip() == "":
            split_point = index
    return lines[:split_point], lines[split_point+1:]


def process_stacks(stacks):
    processed_stacks = {}
    for index, number in enumerate(stacks[-1]):
        if number != " ":
            processed_stacks[number] = {"index": index, "list": []}
    for data in processed_stacks.values():
        for level in stacks[::-1][1:]:
            if data["index"] < len(level):
                if level[data["index"]] != " ":
                    data["list"].append(level[data["index"]])
    return processed_stacks


def read_instruction(instruction):
    instruction = instruction[5:]
    x = instruction.split("from")
    y = x[1].split("to")
    num_to_move = int(x[0].strip())
    from_stack = y[0].strip()
    to_stack = y[1].strip()
    return num_to_move, from_stack, to_stack


def follow_instructions(stacks, instructions):
    for inst in instructions:
        num_to_move, from_stack, to_stack = read_instruction(inst)
        for _ in range(num_to_move):
            item_in_crane = stacks[from_stack]["list"].pop(-1)
            stacks[to_stack]["list"].append(item_in_crane)
    return stacks


def get_output(stacks):
    output = [x["list"][-1] for x in stacks.values()]
    return "".join(output)


def part_2(file_path):
    lines = read_in_file(file_path)
    stacks, instructions = split_input(lines)
    stacks_dict = process_stacks(stacks)
    follow_instructions_2(stacks_dict, instructions)
    return get_output(stacks_dict)


def follow_instructions_2(stacks, instructions):
    for inst in instructions:
        num_to_move, from_stack, to_stack = read_instruction(inst)
        temp_list = []
        for _ in range(num_to_move):
            item_in_crane = stacks[from_stack]["list"].pop(-1)
            temp_list.append(item_in_crane)
        for item_in_crane in temp_list[::-1]:
            stacks[to_stack]["list"].append(item_in_crane)
    return stacks


if __name__ == "__main__":
    print("Part 1")
    print("Example:", part_1("example.txt"))
    print("Real   :", part_1("input.txt"))
    print("\nPart 2")
    print("Example:", part_2("example.txt"))
    print("Real   :", part_2("input.txt"))
