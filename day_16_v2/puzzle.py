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

    def calc_pressure_released(self, current_valve: Valve, opened_valves, time_remaining):
        pressure_released = 0
        if current_valve in opened_valves:
            pressure_released = self.nodes[current_valve].height * (time_remaining)
        best_pressure_released = 0
        if time_remaining <= 0:
            return 0
        for new_valve in self.nodes[current_valve].out_links:
            if new_valve in opened_valves:
                continue
            if (try_pressure := pressure_released + self.calc_pressure_released(
                    new_valve, [*opened_valves, current_valve], time_remaining - 2
            )) > best_pressure_released:
                best_pressure_released = try_pressure
            if (try_pressure := pressure_released + self.calc_pressure_released(
                    new_valve, opened_valves, time_remaining - 1
            )) > best_pressure_released:
                best_pressure_released = try_pressure
        return best_pressure_released

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
    return v.calc_pressure_released("AA", [], 30)


def part_2(file_path):
    return ""


if __name__ == "__main__":
    import faulthandler


    faulthandler.enable()
    print_output(part_1, part_2)

