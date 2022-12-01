def main(file_path):
    input_lines = read_in_calories_file(file_path)
    all_calories = sum_up_calories_by_elf(input_lines)

    print(f"Most calories carried by a single elf: {max(all_calories)}")
    sorted_cals = sorted(all_calories, reverse=True)
    print(f"Total calories carried by top 3 elves: {sorted_cals[0] + sorted_cals[1] + sorted_cals[2]}")


def sum_up_calories_by_elf(input_lines):
    """
    Take a list of data, each element being a string representing each line of the input file (with no \n characters)
    Sum up the numbers between each blank line, and append these sums to a new list
    :param input_lines: List of calories in each food item carried by the elves. Elves are separated by a blank entry
    :return: List of calories carried by each elf, each element represents one elf
    """
    all_calories = [0]
    for line in input_lines:
        if line != "":
            all_calories[-1] += int(line)
        else:
            all_calories.append(0)
    return all_calories


def read_in_calories_file(file_path):
    """
    Read in text file at file path, then split to a list on the newline (\n) character
    :param file_path: Local file path to read in
    :return: List of strings, each element is one line from the input file.
    """
    with open(file_path) as f:
        input_lines = f.read()
        input_lines = input_lines.split("\n")
    return input_lines


if __name__ == "__main__":
    print("Example")
    main("part_1_example.txt")

    print("\nPuzzle")
    main("input.txt")
