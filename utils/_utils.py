

def read_in_file(file_path):
    """
    Read in text file at file path, then split to a list on the newline (\n) character
    :param file_path: Local file path to read in
    :return: List of strings, each element is one line from the input file.
    """
    with open(file_path) as f:
        input_lines = f.read()
        input_lines = input_lines.split("\n")
    return input_lines

def print_output(part_1, part_2):
    print("Part 1")
    print("Example:", part_1("example.txt"))
    print("Real   :", part_1("input.txt"))
    print("\nPart 2")
    print("Example:", part_2("example.txt"))
    print("Real   :", part_2("input.txt"))


def draw_grid(grid):
    return "\n".join([" ".join(str(x) for x in row) for row in grid])


class NTuple(list):
    def __init__(self, args, data_type=None):
        if data_type is not None:
            super().__init__(map(data_type, args))
        else:
            super().__init__(args)
        self.length = len(args)

    @property
    def x(self):
        if self.length > 0:
            return self[0]
        raise IndexError(f"NTuple of length {self.length} has no x component")

    @property
    def y(self):
        if self.length > 1:
            return self[1]
        raise IndexError(f"NTuple of length {self.length} has no x component")

    @property
    def z(self):
        if self.length > 2:
            return self[2]
        raise IndexError(f"NTuple of length {self.length} has no x component")

    def __add__(self, other):
        if self.length != other.length:
            raise ValueError("Cannot add NTuples of different size")
        return type(self)([self[i] + other[i] for i in range(self.length)])

    def __sub__(self, other):
        if self.length != other.length:
            raise ValueError("Cannot add NTuples of different size")
        return type(self)([self[i] - other[i] for i in range(self.length)])

    def __eq__(self, other):
        if self.length != other.length:
            return False
        return all((self[i] == other[i] for i in range(self.length)))

    def __hash__(self):
        return tuple(self).__hash__()


class Pair(list):

    def __init__(self, x, y):
        super().__init__((x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def t(self):
        return Pair(self.y, self.x)

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


class Node:
    def __init__(self, height, coords, out_links=None, in_links=None, distance=1e7, sp_tree=False):
        self.height = height
        self.coords = coords
        self.out_links = [] if out_links is None else out_links
        self.in_links = [] if in_links is None else in_links
        self.distance = distance
        self.visited = False
        self.cheapest_path = []


class Graph:
    def __init__(self, nodes={}, edges=[]):
        self.nodes = {n.coords: n for n in nodes.values()}
        self.edges = edges
        self.start = None
        self.end = None

    def add_node(self, height, coords, out_links=[]):
        if height == "S":
            self.start = coords
            self.nodes[coords] = Node("a", coords, out_links, distance=0, sp_tree=True)
            self.nodes[coords].cheapest_path = [coords]
            return
        if height == "E":
            self.end = coords
            height = "z"
        self.nodes[coords] = Node(height, coords, out_links)

    def populate_links(self):
        for node in self.nodes.values():
            adjacent_nodes = [node.coords + dir_vector for dir_vector in DIRECTION_VECTORS.values()]
            for adj_node in adjacent_nodes:
                if adj_node in self.nodes:
                    if ord(self.nodes[adj_node].height) - 1 <= ord(node.height):
                        node.out_links.append(adj_node)

    def reverse_links(self):
        for node in self.nodes.values():
            adjacent_nodes = [node.coords + dir_vector for dir_vector in DIRECTION_VECTORS.values()]
            for adj_node in adjacent_nodes:
                if adj_node in self.nodes:
                    if ord(self.nodes[adj_node].height) + 1 >= ord(node.height):
                        node.in_links.append(adj_node)

    def find_route(self, current_node=None):
        while current_node != self.end:

            if current_node is None:
                current_node = self.nodes[self.start]
            else:
                current_node = self.nodes[current_node]
            current_node.visited = True
            for adj_node_coords in current_node.out_links:
                adj_node = self.nodes[adj_node_coords]
                if current_node.distance + 1 < adj_node.distance:
                    adj_node.distance = current_node.distance + 1
                    adj_node.cheapest_path = current_node.cheapest_path
                    adj_node.cheapest_path.append(current_node.coords)
            to_visit = {node.coords: node.distance for node in self.nodes.values() if not node.visited}
            if not to_visit:
                break
            current_node = min(to_visit, key=to_visit.get)

    def find_reverse(self, current_node=None):
        to_visit = {node.coords: node.distance for node in self.nodes.values() if not node.visited}
        while to_visit:
            if current_node is None:
                current_node = self.nodes[self.end]
            else:
                current_node = self.nodes[current_node]
            current_node.visited = True
            for adj_node_coords in current_node.in_links:
                adj_node = self.nodes[adj_node_coords]
                if current_node.distance + 1 < adj_node.distance:
                    adj_node.distance = current_node.distance + 1
                    adj_node.cheapest_path = current_node.cheapest_path
                    adj_node.cheapest_path.append(current_node.coords)
            to_visit = {node.coords: node.distance for node in self.nodes.values() if not node.visited}
            if not to_visit:
                break
            current_node = min(to_visit, key=to_visit.get)

DIRECTION_VECTORS = {
    "R": Pair(1, 0),
    "L": Pair(-1, 0),
    "U": Pair(0, 1),
    "D": Pair(0, -1)
}
