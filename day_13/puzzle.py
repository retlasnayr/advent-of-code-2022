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
            left = Packet(pair[0])
            right = Packet(pair[1])
            if left < right:
                total += index
    return total


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
        self.string = packet_string
        loc = {}
        exec(f"packet = {packet_string}", globals(), loc)
        self.auto_value = loc["packet"]
        val = self.parse_list()[0]
        self.value = val
        if self.value != self.auto_value:
            raise ValueError("HELP!!")

    def parse_list(self, start=0, end=None):
        just_appended = False
        return_list = []
        for index, character in enumerate(self.string):
            if index < start:
                just_appended = False
                continue
            if character == ",":
                just_appended = False
                continue
            if character == "]":
                just_appended = False
                return return_list, index+1
            if character == "[":
                just_appended = False
                temp, start = self.parse_list(index+1)
                return_list.append(temp)
                continue
            if just_appended:
                return_list[-1] = int(str(return_list[-1]) + character)  # This is hacky but otherwise [10,2] -> [1,0,2]
            else:
                return_list.append(int(character))
                just_appended = True

        return return_list

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
    # print([packet.value for packet in sorted_packets])
    return (sorted_packets.index(div1) + 1) * (sorted_packets.index(div2) + 1)


if __name__ == "__main__":
    print_output(part_1, part_2)
    # import timeit
    #
    # print(timeit.timeit(lambda: part_2('input.txt'), number=1000))

