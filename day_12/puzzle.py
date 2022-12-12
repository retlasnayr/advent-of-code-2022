from utils import read_in_file, print_output, draw_grid, Pair, DIRECTION_VECTORS


OPPOSITE = {
    "U": "D",
    "D": "U",
    "L": "R",
    "R": "L"
}

def compare_heights(current, target):
    return ord(target) - ord(current) <= 1


class Node:
    def __init__(self, height, coords, out_links=None, in_links=None, distance=1e7, sp_tree=False):
        self.height = height
        self.coords = coords
        self.out_links = [] if in_links is None else out_links
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



class Grid:
    def __init__(self, lines):
        self.height = None
        self.width = None
        self.data = None
        self.start_location = None
        self.end_location = None
        self.routes = []
        self.graph = Graph()

        self.from_lines(lines)


    def from_lines(self, lines):
        self.data = [[x for x in line] for line in lines]
        self.width = len(lines[0])
        self.height = len(lines)
        self.build_graph()

    def build_graph(self):
        for row_index, row in enumerate(self.data):
            for col_index, col in enumerate(row):
                self.graph.add_node(col, Pair(col_index, row_index))
        self.graph.populate_links()
        self.graph.reverse_links()

    def row(self, n):
        return self.data[n]

    def column(self, n):
        return [x[n] for x in self.data]

    def cell_value(self, coords: Pair):
        if coords[0] < 0 or coords[0] >= self.width or coords[1] < 0 or coords[1] >= self.height:
            raise ValueError("Cell index out of grid")
        return self.data[coords[1]][coords[0]]

    def get_adjacent(self, direction, current_location):
        loc = current_location + DIRECTION_VECTORS[direction]
        return loc, self.cell_value(loc)

    def print_route(self, route):
        grid_pic = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for num, pair in enumerate(route[:-1]):
            direction = {Pair(0, 1): "v", Pair(1, 0): ">", Pair(-1, 0): "<", Pair(0, -1): "^"}[route[num+1]-pair]
            grid_pic[pair[1]][pair[0]] = direction
        return draw_grid(grid_pic)




def part_1(file_path):
    lines = read_in_file(file_path)
    grid = Grid(lines)
    grid.graph.find_route()
    return grid.graph.nodes[grid.graph.end].distance
    # print("\n")
    # # print(grid.print_route(grid.routes[0]))
    # # print(grid.routes)
    # return(min([len(x) for x in grid.routes]) -1)


def part_2(file_path):
    lines = read_in_file(file_path)

    clean_lines = [line.replace("S", "a") for line in lines]
    grid = Grid(lines)
    grid.graph.nodes[grid.graph.end].distance = 0
    grid.graph.nodes[grid.graph.start].distance = 1e5
    grid.graph.find_reverse(grid.graph.end)
    lengths = [x.distance for x in grid.graph.nodes.values() if x.height == "a"]
    return min(lengths)


if __name__ == "__main__":
    print_output(part_1, part_2)
