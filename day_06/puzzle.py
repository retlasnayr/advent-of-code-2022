from utils import read_in_file, print_output


def part_1(file_path):
    lines = read_in_file(file_path)
    for line in lines:
        print(n_distinct_chars(line, 4))


def n_distinct_chars(line, n):
    buffer = []
    for index, character in enumerate(line):
        if len(buffer) == n:
            if len(set(buffer)) == n:
                return index
            buffer.pop(0)
        buffer.append(character)

def part_2(file_path):
    lines = read_in_file(file_path)
    for line in lines:
        print(n_distinct_chars(line, 14))


if __name__ == "__main__":
    print_output(part_1, part_2)

