from utils import read_in_file, print_output, draw_grid


class CRT:
    def __init__(self):
        self.x_register = 1
        self.clock = 0
        self.signal_strengths = []
        self.display = [["." for _ in range(40)] for _ in range(6)]

    def tick(self):
        self.clock += 1
        if self.clock % 40 - self.x_register in (-1, 0, 1):
            self.display[self.clock // 40][self.clock % 40] = "#"


        if self.clock % 40 == 20:
            self.signal_strengths.append(self.clock * self.x_register)
    def add_x(self, summand):
        self.tick()
        self.x_register += int(summand)
        self.tick()

    def print_display(self):
        print(draw_grid(self.display))


def part_1(file_path):
    lines = read_in_file(file_path)
    crt = CRT()
    for line in lines:
        process_line(line, crt)
    print(crt.signal_strengths)
    return sum(crt.signal_strengths)


def process_line(line, crt):
    instruction = line[:4]
    if "noop" == instruction:
        crt.tick()
    if "addx" == instruction:
        summand = line.split(" ")[1]
        crt.add_x(summand)

def part_2(file_path):
    lines = read_in_file(file_path)
    crt = CRT()
    for line in lines:
        process_line(line, crt)
    crt.print_display()

if __name__ == "__main__":
    print_output(part_1, part_2)

