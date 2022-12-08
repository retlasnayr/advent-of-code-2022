from utils import read_in_file, print_output


def part_1(file_path):
    raw_data = read_in_file(file_path)
    proc_data = [[int(x) for x in row] for row in raw_data]
    visible_trees = 0
    for row_index, row in enumerate(proc_data):
        for col_index, _ in enumerate(row):
            if is_visible(row_index, col_index, proc_data):
                visible_trees += 1
    return visible_trees


def is_visible(row_index: int, col_index: int, grid: list[list[int]]):
    if is_edge(row_index, col_index, grid):
        return True
    if look_right(grid[row_index], col_index)[0]:
        return True
    if look_left(grid[row_index], col_index)[0]:
        return True
    if look_up([row[col_index] for row in grid], row_index)[0]:
        return True
    if look_down([row[col_index] for row in grid], row_index)[0]:
        return True
    return False


def is_edge(row_index, col_index, grid):
    if row_index in (0, len(grid[0])-1) or col_index in (0, len(grid)-1):
        return True
    return False


def look_right(row_data, col_index):
    return look_along(row_data[col_index+1:], row_data[col_index])


def look_left(row_data, col_index):
    return look_along(row_data[:col_index][::-1], row_data[col_index])


def look_up(col_data, row_index):
    return look_along(col_data[:row_index][::-1], col_data[row_index])


def look_down(col_data, row_index):
    return look_along(col_data[row_index+1:], col_data[row_index])


def look_along(data_list, tree_height):
    distance = 0
    for distance, item in enumerate(data_list):
        if tree_height <= item:
            return False, distance + 1
    return True, distance + 1


def look_for_trees(row_index: int, col_index: int, grid: list[list[int]]):
    score = 1
    if is_edge(row_index, col_index, grid):
        return 0
    score *= look_right(grid[row_index], col_index)[1]
    score *= look_left(grid[row_index], col_index)[1]
    score *= look_up([row[col_index] for row in grid], row_index)[1]
    score *= look_down([row[col_index] for row in grid], row_index)[1]
    return score


def part_2(file_path):
    raw_data = read_in_file(file_path)
    proc_data = [[int(x) for x in row] for row in raw_data]
    scores = []
    for row_index, row in enumerate(proc_data):
        for col_index, _ in enumerate(row):
            scores.append(look_for_trees(row_index, col_index, proc_data))
    return max(scores)


if __name__ == "__main__":
    print_output(part_1, part_2)

