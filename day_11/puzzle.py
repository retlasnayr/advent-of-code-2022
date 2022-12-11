from utils import read_in_file, print_output, draw_grid


class Monkey:
    def __init__(self, items: list = [], operation: str = "", test: int = 1):
        self.items = items
        self.operation = None
        self.test = test
        self.true_target = None
        self.false_target = None
        self.items_inspected = 0


    def set_operation(self, operation):
        operation = operation.split(" ")
        lhs, operation, rhs = operation
        try:
            clean_lhs = int(lhs)
        except ValueError:
            clean_lhs = None
        try:
            clean_rhs = int(rhs)
        except ValueError:
            clean_rhs = None
        self.operation = (clean_lhs, operation, clean_rhs)

    def do_operation(self, old_item):
        lhs, rhs = old_item, old_item

        if self.operation[0] is not None:
            lhs = self.operation[0]
        if self.operation[2] is not None:
            rhs = self.operation[2]
        match self.operation[1]:
            case "+":
                return lhs + rhs
            case "-":
                return lhs - rhs
            case "*":
                return lhs * rhs

    def do_test(self, worry_value):
        if worry_value % self.test == 0:
            return self.true_target
        return self.false_target

    def inspect_item(self):
        self.items_inspected += 1
        old_item = self.items.pop(0)
        new_level = self.do_operation(old_item)
        new_level //= 3
        target = self.do_test(new_level)
        return target, new_level


class Monkeys:

    def __init__(self, lines):
        self.monkeys = self.setup_monkeys(lines)

    def setup_monkeys(self, lines):
        monkeys = {}
        for line in lines:
            if "Monkey" in line:
                monkey_number = line.split(" ")[1][:-1]
                monkeys[monkey_number] = Monkey()
            elif "Starting items: " in line:
                items = line.split(": ")[1]
                monkeys[monkey_number].items = [int(x) for x in items.split(", ")]
            elif "Operation: " in line:
                op = line.split(": ")[1]
                f = op.split(" = ")[1]
                monkeys[monkey_number].set_operation(f)
            elif "Test: " in line:
                test = line.split(": ")[1]
                if "divisible by" in test:
                    monkeys[monkey_number].test = int(test.split(" ")[-1])
                else:
                    raise ValueError(test)
            elif "If true" in line:
                monkeys[monkey_number].true_target = line.split(" ")[-1]
            elif "If false" in line:
                monkeys[monkey_number].false_target = line.split(" ")[-1]
        return monkeys

    def perform_round(self):
        for monkey in self.monkeys.values():
            while len(monkey.items) > 0:
                target, item = monkey.inspect_item()
                self.monkeys[target].items.append(item)

    def create_output(self):
        inspected = [v.items_inspected for v in self.monkeys.values()]
        inspected = sorted(inspected, reverse=True)
        return inspected[0] * inspected[1]



def part_1(file_path):
    lines = read_in_file(file_path)
    monkeys = Monkeys(lines)

    for _ in range(20):
        monkeys.perform_round()
    return monkeys.create_output()




def part_2(file_path):
    return ""
    # lines = read_in_file(file_path)
    # lines = read_in_file(file_path)
    # monkeys = setup_monkeys(lines)
    # for i in range(20):
    #     print(i)
    #     for _ in range(20):
    #         monkeys = perform_round(monkeys)
    # inspected = [v.items_inspected for v in monkeys.values()]
    # inspected = sorted(inspected, reverse=True)
    # return inspected[0] * inspected[1]


if __name__ == "__main__":
    print_output(part_1, part_2)

