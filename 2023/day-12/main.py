import sys
from functools import lru_cache


def replace_index(string: str, index: int, value: str):
    return string[:index] + value + string[index + 1:]


@lru_cache(maxsize=None)
def validate(source: str, numbers):
    if len(numbers) == 0:
        if source.find("#") == -1:
            return 1
        return 0

    if len(source) <= 0:
        return 0

    if source[0] == ".":
        return validate(source[1:], numbers)

    if source[0] == "?":
        return validate("#" + source[1:], numbers) + validate("." + source[1:], numbers)

    if source[0] == "#":
        current_group_len = int(numbers[0])
        if len(source) < current_group_len:
            return 0
        for i in range(current_group_len):
            if source[i] == ".":
                return 0
        if current_group_len != len(source) and source[current_group_len] == "#":
            return 0

        return validate(source[current_group_len + 1:], numbers[1:])


@lru_cache(maxsize=None)
def try_fit(source_string, target_numbers):
    source_numbers = list(filter(lambda v: v != 0, [len(value) for value in source_string.split(".")]))

    if len(source_numbers) != len(target_numbers):
        return False

    for n1, n2 in zip(source_numbers, target_numbers):
        if n1 != n2:
            return False

    return True


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != ""]

    variations = []

    for line in lines:
        symbols_string, numbers_string = line.split(" ")
        numbers = [int(number) for number in numbers_string.split(",")]
        target_string = ".".join(list(filter(lambda v: len(v), symbols_string.split("."))))
        # print(numbers, target_string)

        variations.append(validate(target_string, tuple(numbers)))

    return sum(variations)


def task2(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != ""]

    variations = []

    for line in lines:
        symbols_string, numbers_string = line.split(" ")
        numbers = [int(number) for number in numbers_string.split(",")]
        symbols_string = "..." + "?".join([symbols_string] * 5) + "..."
        symbols = list(filter(lambda v: len(v), symbols_string.split(".")))
        numbers = numbers + numbers + numbers + numbers + numbers

        # print(numbers, ".".join(symbols))
        result = validate(".".join(symbols), tuple(numbers))
        variations.append(result)

    return sum(variations)


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2(path)))
