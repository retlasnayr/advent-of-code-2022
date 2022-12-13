from utils import read_in_file, print_output, draw_grid


def part_1(file_path):
    lines = read_in_file(file_path)
    index = 1
    pair = []
    total = 0
    for line in lines:
        if line == "":
            pair = []
            index += 1
        else:
            pair.append(line)
        if len(pair) == 2:
            if compare_pair(pair[0], pair[1]):
                total += index
    return total


def compare_pair(left_in, right_in):
    loc = {}
    exec(f"left = {left_in}", globals(), loc)
    exec(f"right = {right_in}", globals(), loc)
    return compare(loc["left"], loc["right"])

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    if isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]
    if isinstance(left, list) and isinstance(right, list):
        for index in range(min(len(left),len(right))):
            comp = compare(left[index], right[index])
            if comp is None:
                continue
            return comp
        if len(left) == len(right):
            return None
        return len(left) < len(right)


class Packet:
    def __init__(self, packet_string):
        loc = {}
        exec(f"packet = {packet_string}", globals(), loc)
        self.value = loc["packet"]

    def __lt__(self, other):
        if not isinstance(other, Packet):
            raise ValueError(f"Cannot compare Packet to {type(other)} type object.")
        comp = compare(self.value, other.value)
        if comp is not None:
            return comp
        if self == other:
            return False
        raise ValueError(f"Comparison of packets {self}, {other} failed.")

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        if not isinstance(other, Packet):
            raise ValueError(f"Cannot compare Packet to {type(other)} type object.")
        return other < self

    def __ge__(self, other):
        return self > other or self == other

    def __eq__(self, other):
        if not isinstance(other, Packet):
            return False
        return self.value == other.value


def part_2(file_path):
    lines = read_in_file(file_path)
    div1 = Packet("[[2]]")
    div2 = Packet("[[6]]")
    packets = [div1, div2]
    for line in lines:
        if line == "":
            continue
        packets.append(Packet(line))
    sorted_packets = sorted(packets)
    print([packet.value for packet in sorted_packets])
    return (sorted_packets.index(div1) + 1) * (sorted_packets.index(div2) + 1)


if __name__ == "__main__":
    print_output(part_1, part_2)

