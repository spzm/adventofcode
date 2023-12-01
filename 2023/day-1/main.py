import re
import sys

WRITTEN_NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def find_all_positions(positions: list[int | None], line: str, substr: str, number: int):
    found = True
    last_index = -1
    while found:
        found = False
        position = line.find(substr, last_index + 1)
        if position != -1:
            positions[position] = number
            last_index = position
            found = True

    return positions


def replace_numbers(line: str):
    positions = [None for symbol in line]

    for i, number in enumerate(WRITTEN_NUMBERS):
        find_all_positions(positions, line, number, i + 1)
        find_all_positions(positions, line, str(i + 1), i + 1)

    return str(positions)


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    all_numbers = [re.sub(r"\D", "", line) for line in lines]
    calibration_numbers = [int(number[0] + number[-1]) for number in all_numbers]

    return sum(calibration_numbers)


def task2(file_name: str):
    file = open(file_name, "r")
    lines = [replace_numbers(line.strip()) for line in file if line != '']

    all_numbers = [re.sub(r"\D", "", line) for line in lines]
    calibration_numbers = [int(number[0] + number[-1]) for number in all_numbers]

    return sum(calibration_numbers)


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2(path)))
