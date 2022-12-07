from utils import read_in_file, print_output
from collections import defaultdict


def part_1(file_path):
    lines = read_in_file(file_path)
    dirs = iter_lines(lines)
    print(dirs)
    return sum_up_sizes(dirs)[1]


def iter_lines(lines):
    curr_path = []
    dirs = defaultdict(list)
    fs = {}
    listing = False
    for line in lines:
        line = line.split(" ")
        if line[0] == "$":
            listing = False
            if line[1] == "cd":
                if line[2] == "/":
                    curr_path = ["/"]
                elif line[2] == "..":
                    curr_path.pop(-1)
                else:
                    curr_path.append(" ".join(line[2:]))
            elif line[1] == "ls":
                listing = True
        elif listing:

            if line[0] == "dir":
                get_cwd(curr_path, fs)["subdirs"].append(" ".join(line[1:]))
            else:
                get_cwd(curr_path, fs)["files"].append({"name": " ".join(line[1:]), "size": int(line[0])})
                for index, _ in enumerate(curr_path):
                    dirs["/".join(curr_path[:index+1])].append({"name": " ".join(line[1:]), "size": int(line[0])})
    return dirs


def get_cwd(curr_path, fs):
    temp_fs = fs
    for item in curr_path:
        if item in temp_fs:
            temp_fs = temp_fs[item]
        else:
            temp_fs[item] = {"subdirs": [], "files": []}
            return temp_fs[item]
    return temp_fs


def sum_up_sizes(dirs):
    total_size = 0
    sizes = {}
    for dir_name, dir_data in dirs.items():
        size = sum(x["size"] for x in dir_data)
        sizes[dir_name] = size
        if size <= 100000:
            total_size += size
    print(sizes)
    return sizes, total_size


def part_2(file_path):
    lines = read_in_file(file_path)
    dirs = iter_lines(lines)
    sizes = sum_up_sizes(dirs)[0]
    free_space = 70000000 - sizes["/"]
    required_space = 30000000 - free_space
    candidates = {name: size for name, size in sizes.items() if size >= required_space}
    best = min(candidates.values())
    return best


if __name__ == "__main__":
    print_output(part_1, part_2)

