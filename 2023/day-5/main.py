import re
import sys


def in_range(source, diff, value):
    min_source = source
    max_source = source + diff

    return min_source <= value < max_source


def parse_file(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    seeds = [int(value) for value in lines[0].split(":")[1].split()]

    groups = []

    group = None
    for line in lines[2:]:
        if not line:
            continue

        if line.strip().endswith(":"):
            if group:
                groups.append(group)
            group = []
            continue

        group.append([int(value) for value in line.split()])
    groups.append(group)

    return seeds, groups


def task1(file_name: str):
    seeds, groups = parse_file(file_name)

    locations = []
    location_histories = []

    for seed in seeds:
        location = seed
        location_history = [seed]
        for group in groups:
            is_found = False
            for ranges in group:
                [destination, source, diff] = ranges

                if in_range(source, diff, location):
                    is_found = True
                    location = destination + location - source
                    location_history.append(location)
                    break
            if not is_found:
                location_history.append(location)
        locations.append(location)
        location_histories.append(location_history)

    return min(locations)


def task2(file_name: str, ii: int, jj: int):
    seeds, groups = parse_file(file_name)

    seeds = seeds[4:]

    grouped_seeds = list(zip(seeds[::2], seeds[1::2]))
    sorted_seeds = sorted(grouped_seeds, key=lambda x: x[0])
    sorted_seeds = [[value[0], value[0] + value[1]] for value in sorted_seeds]

    selected_seeds = sorted_seeds[ii:jj]

    min_location = None
    min_seed = None

    for [min_value, max_value] in selected_seeds:
        it = 1
        print("total to run: %s", max_value - min_value)
        for seed in range(min_value, max_value):
            it = it + 1
            location = seed
            for group in groups:
                for ranges in group:
                    if in_range(ranges[1], ranges[2], location):
                        location = ranges[0] + location - ranges[1]
                        break

            if not min_location or location < min_location:
                min_location = location
                min_seed = seed

            if it % 100000 == 0:
                print("iteration %s", it)

    return min_location, min_seed


if __name__ == "__main__":
    path = sys.argv[1]
    i = int(sys.argv[2])
    j = int(sys.argv[3])

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2(path, i, j)))
