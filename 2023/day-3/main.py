import sys
from typing import Callable


def check_index(x, y, lines, check_predicate: Callable[[str], bool]):
    if x < 0 or y < 0 or x > len(lines) - 1 or y > len(lines[0]) - 1:
        return None

    return check_predicate(lines[x][y]), x, y


def check_neighbours(x: int, y: int, lines: list[str], check_predicate: Callable[[str], bool]):
    x_diff = [-1, 0, 1]
    y_diff = [-1, 0, 1]

    for x_d in x_diff:
        for y_d in y_diff:
            if x_d == 0 and y_d == 0:
                continue

            check_result = check_index(x + x_d, y + y_d, lines, check_predicate)
            if check_result and check_result[0]:
                return check_result
    return None


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    numbers = []

    for x, line in enumerate(lines):
        number = []
        is_island = False
        for y, symbol in enumerate(lines[x]):
            if symbol.isdigit():
                number.append(symbol)
                if not is_island and check_neighbours(x, y, lines,
                                                      check_predicate=lambda s: s != "." and not s.isdigit()):
                    is_island = True
            else:
                if len(number):
                    if is_island:
                        numbers.append(int("".join(number)))
                number = []
                is_island = False

        if len(number):
            if is_island:
                numbers.append(int("".join(number)))

    return sum(numbers)


def task2(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    numbers = {}

    for x, line in enumerate(lines):
        number = []
        x_index = 0
        y_index = 0

        is_island = False
        for y, symbol in enumerate(lines[x]):
            if symbol.isdigit():
                number.append(symbol)
                if not is_island:
                    check_result = check_neighbours(x, y, lines, check_predicate=lambda s: s == "*")
                    if check_result:
                        is_island = True
                        x_index = check_result[1]
                        y_index = check_result[2]

            else:
                if len(number):
                    if is_island:
                        key = f"{x_index}_{y_index}"
                        if not numbers.get(key):
                            numbers[key] = []
                        numbers[key].append(int("".join(number)))
                number = []
                x_index = -1
                y_index = -1
                is_island = False

        if len(number):
            key = f"{x_index}_{y_index}"
            if not numbers.get(key):
                numbers[key] = []
            numbers[key].append(int("".join(number)))

    total = 0
    for mul in numbers.values():
        if len(mul) == 2:
            total = total + mul[0] * mul[1]

    return total


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2(path)))
#
