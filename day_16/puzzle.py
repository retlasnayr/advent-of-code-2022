from utils import read_in_file, print_output, draw_grid, Graph, Node


class Valve(Node):

    def __init__(self, name, flow_rate, tunnels):
        super().__init__(flow_rate, name, out_links=tunnels)

class Volcano:

    def __init__(self, lines):
        self.start_valve = "AA"
        self.time_remaining = 30
        self.total_outflow = 0
        self.tunnels = []
        self.nodes = self.from_lines(lines)
        self.paths = self.calc_paths()

    def calc_paths(self):
        paths = {}
        for valve1 in self.nodes:
            paths[valve1] = {}
            for valve2 in self.nodes:
                v1v2_distance = self.shortest_path(self.nodes[valve1], self.nodes[valve2])
                paths[valve1][valve2] = v1v2_distance
        return paths


    def shortest_path(self, valve1, valve2):
        for valve in self.nodes:
            self.nodes[valve].distance = 1e5
        valve1.distance = 0
        self.find_route(valve1, valve1, valve2)
        return valve2.distance

    def find_route(self, current_node=None, start_node=None, target_node=None):
        while current_node.coords != target_node.coords:
            if current_node is None:
                current_node = start_node
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
            min_node = min(to_visit, key=to_visit.get)
            current_node = self.nodes[min_node]

    def valve_outflow(self, valve):
        return valve.rate * self.time_remaining

    def from_lines(self, lines):
        data = {}
        for line in lines:
            valve = self.parse_line(line)
            data[valve.coords] = valve
        return data

    def parse_line(self, line):
        valve_name = line.split(" ")[1]
        rate = int(line.split(";")[0].split("=")[1])
        try:
            tunnels = line.split("valves ")[1].split(", ")
        except IndexError:
            tunnels = [line.split(" ")[-1]]
        self.tunnels.extend([t for t in tunnels])
        return Valve(valve_name, rate, tunnels)





def part_1(file_path):
    lines = read_in_file(file_path)
    v = Volcano(lines)
    print("foo")


def part_2(file_path):
    return ""


if __name__ == "__main__":
    import faulthandler


    faulthandler.enable()
    print_output(part_1, part_2)

