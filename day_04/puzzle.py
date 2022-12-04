from utils import read_in_file


def part_1(file_path):
    lines = read_in_file(file_path)
    overlaps = 0
    for line in lines:
        line = line.split(",")
        line = [x.split("-") for x in line]
        if x_subset_of_y(line[0], line[1]) or x_subset_of_y(line[1], line[0]):
            overlaps += 1
    return overlaps


def x_subset_of_y(x, y):
    if int(x[0]) >= int(y[0]) and int(x[1]) <= int(y[1]):
        return True
    return False


def part_2(file_path):
    lines = read_in_file(file_path)
    overlaps = 0
    for line in lines:
        line = line.split(",")
        line = [x.split("-") for x in line]
        if x_overlaps_y(line[0], line[1]) or x_overlaps_y(line[1], line[0]):
            overlaps += 1
    return overlaps


def x_overlaps_y(x, y):
    if int(y[1]) >= int(x[0]) >= int(y[0]) or int(y[0]) <= int(x[1]) <= int(y[1]):
        return True
    return False


if __name__ == "__main__":
    print("Part 1")
    print("Example:", part_1("example.txt"))
    print("Real   :", part_1("input.txt"))
    print("\nPart 2")
    print("Example:", part_2("example.txt"))
    print("Real   :", part_2("input.txt"))
