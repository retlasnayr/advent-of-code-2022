import day_01

SHAPE_SCORES = {"R": 1, "P": 2, "S": 3}
KEY_BEATS_VAL = {"R": "S", "S": "P", "P": "R"}
VAL_BEATS_KEY = {value: key for key, value in KEY_BEATS_VAL.items()}


def main(file_path):
    strategy = day_01.read_in_calories_file(file_path)
    split_strategy = [x.split(" ") for x in strategy]
    # print(split_strategy)
    my_total_score = 0
    for turn in split_strategy:
        if turn != ['']:
            my_total_score += play_round(turn)
    print(my_total_score)


def play_round(strategy: tuple[str, str]):
    elf, me = strategy
    elf, me = map_to_RPS(elf), map_to_RPS(me)
    my_score = SHAPE_SCORES[me]
    round_score = calc_score(elf, me)
    my_score += round_score[1]
    return my_score


def map_to_RPS(character):
    if character in ("A", "X"):
        return "R"
    if character in ("B", "Y"):
        return "P"
    if character in ("C", "Z"):
        return "S"


def calc_score(p1, p2):
    if p1 == p2:
        return (3, 3)
    if KEY_BEATS_VAL[p1] == p2:
        return (6, 0)
    else:
        return (0, 6)


def correct_method(strategy):
    elf = map_to_RPS(strategy[0])
    result = strategy[1]
    score = 0
    if result == "Y":  # Draw
        me = elf
        score += 3
    elif result == "X":  # Lose
        me = KEY_BEATS_VAL[elf]
    elif result == "Z":  # Win
        me = VAL_BEATS_KEY[elf]
        score += 6
    score += SHAPE_SCORES[me]
    return score

if __name__ == "__main__":
    main("example")
    main("input.txt")