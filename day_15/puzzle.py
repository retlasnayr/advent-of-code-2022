from utils import read_in_file, print_output, draw_grid, Pair


def manhattan_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def parse_line(line):
    line = line.split(" ")
    sensor = Pair(int(line[2].split("=")[1][:-1]), int(line[3].split("=")[1][:-1]))
    beacon = Pair(int(line[8].split("=")[1][:-1]), int(line[9].split("=")[1]))
    return sensor, beacon



def part_1(file_path):
    lines = read_in_file(file_path)
    sensors = {}
    beacons = set()
    for line in lines:
        s, b = parse_line(line)
        sensors[s] = {"closest_beacon": b, "dist": manhattan_dist(s, b)}
        beacons.add(b)
    min_x = min(sensors, key=lambda x: x.x).x
    max_x = max(sensors, key=lambda x: x.x).x
    dist = [x['dist'] for x in sensors.values()]
    max_dist = max(dist)
    min_x -= max_dist
    max_x += max_dist
    if "example" in file_path:
        y = 10
    else:
        y = 2000000
    clear_positions = 0
    for x in range(min_x, max_x + 1):
        clear = False
        for sensor, sensor_data in sensors.items():
            if manhattan_dist(Pair(x, y), sensor) <= sensor_data["dist"] and Pair(x, y) not in beacons:
                clear = True
        if clear:
            clear_positions += 1
        # print(x, clear)
    return clear_positions


def part_1_v2(file_path):
    lines = read_in_file(file_path)
    sensors = {}
    beacons = set()
    for line in lines:
        s, b = parse_line(line)
        sensors[s] = {"closest_beacon": b, "dist": manhattan_dist(s, b)}
        beacons.add(b)
    if "example" in file_path:
        y = 10
    else:
        y = 2000000
    clear = set()
    for sensor, data in sensors.items():
        y_dist = abs(sensor.y - y)
        x_range = data["dist"] - y_dist
        xes = range(sensor.x - x_range, sensor.x + x_range + 1)
        clear_candidates = {Pair(x, y) for x in xes}
        clear = clear.union(clear_candidates)
    for beacon in beacons:
        if beacon in clear:
            clear.remove(beacon)
    return len(clear)
def part_2(file_path):
    lines = read_in_file(file_path)
    sensors = {}
    beacons = set()
    for line in lines:
        s, b = parse_line(line)
        sensors[s] = {"closest_beacon": b, "dist": manhattan_dist(s, b)}
        beacons.add(b)
    if "example" in file_path:
        y = 10
        max_coord = 20
    else:
        y = 2000000
        max_coord = 4000000
    possible_locations = set()

    for sensor, data in sensors.items():
        print(sensor)
        dist = data["dist"]
        # print(draw_grid([["#" if Pair(x1, y1) in possible_locations else "." for x1 in range(max_coord)] for y1 in range(max_coord)]))
        # print("\n")
        movement_vectors = [Pair(x, 1 + dist - x) for x in range(dist + 1)]
        possible_locations = possible_locations.union({sensor + vec for vec in movement_vectors})
        possible_locations = possible_locations.union({sensor - vec for vec in movement_vectors})
        possible_locations = possible_locations.union({sensor + Pair(vec.x, -vec.y) for vec in movement_vectors})
        possible_locations = possible_locations.union({sensor - Pair(vec.x, -vec.y) for vec in movement_vectors})

    bad = set()
    for loc in possible_locations:
        remove = False
        if loc.x < 0 or loc.x > max_coord or loc.y < 0 or loc.y > max_coord:
            remove = True
        else:
            for sensor, data in sensors.items():
                if manhattan_dist(loc, sensor) <= data["dist"]:
                    remove = True
        if remove:
            bad.add(loc)
    for loc in bad:
        try:
            possible_locations.remove(loc)
        except KeyError:
            pass

    results = [item.x * 4000000 + item.y for item in possible_locations]
    return results




if __name__ == "__main__":
    print(part_2("example.txt"))
    # print_output(part_1_v2, part_2)

