from math import lcm
import sys


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    sequence = [*lines[0]]

    nodes_map = {}
    for line in lines[2:]:
        key, value = line.split("=")
        left_right = value.split(",")

        nodes_map[key.strip()] = [left_right[0].strip()[1:], left_right[1].strip()[:-1]]

    repeat_sequence = None
    count = 0
    pattern = "AAA"
    while pattern != "ZZZ":
        if not repeat_sequence:
            repeat_sequence = [*sequence]

        move = 0 if repeat_sequence.pop(0) == "L" else 1

        pattern = nodes_map[pattern][move]

        count = count + 1

    return count


def find_cycle(pattern, sequence, nodes_map):
    repeat_sequence = None
    count = 0

    repeats = []
    starting_point = [pattern]
    new_pattern = pattern

    is_cycled = False
    while not is_cycled:
        if not repeat_sequence:
            repeat_sequence = [*sequence]

            if count != 0 and new_pattern.endswith("Z"):
                is_cycled = True
                continue

        move = 0 if repeat_sequence.pop(0) == "L" else 1

        new_pattern = nodes_map[new_pattern][move]

        count = count + 1
        if new_pattern.endswith("Z"):
            repeats.append(count)

    return count


def task2(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    sequence = [*lines[0]]

    nodes_map = {}
    nodes_patterns = []
    for line in lines[2:]:
        key, value = line.split("=")
        left_right = value.split(",")
        key = key.strip()

        if key.endswith("A"):
            nodes_patterns.append(key)

        nodes_map[key] = [left_right[0].strip()[1:], left_right[1].strip()[:-1]]

    node_cycles = []
    for pattern in nodes_patterns:
        node_cycles.append(find_cycle(pattern, sequence, nodes_map))

    return lcm(*node_cycles)


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2(path)))
