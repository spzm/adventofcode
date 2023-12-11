import sys


def predict_last_line_value(sequence: list[int]):
    all_zeros = False

    lists_levels = [sequence]

    while not all_zeros:
        bottom_level = lists_levels[-1]
        next_level = [int(bottom_level[i + 1] - bottom_level[i]) for i in range(len(bottom_level) - 1)]

        if len(set(next_level)) == 1 and next_level[0] == 0:
            all_zeros = True

        if len(next_level) == 0:
            break

        lists_levels.append(next_level)

    reverted_list = list(reversed(lists_levels))
    last_line = reverted_list[0]
    last_value = last_line[-1]
    first_value = last_line[0]

    for line in reverted_list[1:]:
        last_line_value = line[-1]
        last_value = last_value + last_line_value

        first_line_value = line[0]
        first_value = first_line_value - first_value

    return last_value, first_value


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [[int(value) for value in line.strip().split()] for line in file if line != '']

    first_values = []
    last_values = []
    for line in lines:
        first, last = predict_last_line_value(line)
        first_values.append(first)
        last_values.append(last)

    return sum(first_values), sum(last_values)


def task2(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    return lines


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Tasks: {}'.format(task1(path)))
