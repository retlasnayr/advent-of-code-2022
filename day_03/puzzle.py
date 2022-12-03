from utils import read_in_file


def part_1(path):
    priorities = 0
    input_lines = read_in_file(path)
    for line in input_lines:
        line_length = len(line)
        compartments = (line[:line_length//2], line[line_length//2:])
        char_in_both = matching_chars(compartments)[0]
        # print(char_in_both)
        priorities += score(char_in_both)
    return priorities


def part_2(path):
    priorities = 0
    input_lines = read_in_file(path)
    n = 3
    grouped_lines = [input_lines[i:i+n] for i in range(0, len(input_lines), n)]
    for group in grouped_lines:
        m1 = matching_chars((group[0], group[1]))
        m2 = matching_chars((group[1], group[2]))
        match = matching_chars((m1, m2))[0]
        # print(match)
        priorities += score(match)
    return priorities


def matching_chars(pair):
    matches = []
    for x in pair[0]:
        if x in pair[1]:
            matches.append(x)
    return matches


def score(character):
    if character.upper() == character:
        return ord(character) - ord("A") + 26 + 1
    return ord(character) - ord("a") + 1


if __name__ == "__main__":
    print("Part 1")
    print("Example:", part_1("example.txt"))
    print("Real   :", part_1("input.txt"))
    print("\nPart 2")
    print("Example:", part_2("example.txt"))
    print("Real   :", part_2("input.txt"))
