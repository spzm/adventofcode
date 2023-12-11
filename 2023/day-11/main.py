from pprint import pprint
import sys
import math


def galaxy_distance(p, q, empty_x, empty_y, k=2):
    [x1, y1] = p
    [x2, y2] = q

    x_min = x1 if x1 < x2 else x2
    x_max = x1 if x1 > x2 else x2

    y_min = y1 if y1 < y2 else y2
    y_max = y1 if y1 > y2 else y2

    empty_x = list(filter(lambda value: x_min < value < x_max, empty_x))
    empty_y = list(filter(lambda value: y_min < value < y_max, empty_y))

    return math.fabs(x1 - x2) + math.fabs(y1 - y2) + ((k - 1) * len(empty_x)) + ((k - 1) * len(empty_y))


def task1_2(file_name: str):
    file = open(file_name, "r")
    lines = [[*line.strip()] for line in file if line != '']

    coordinates = []

    empty_x = []
    empty_y = []
    for i in range(len(lines)):
        if len(set(lines[i])) == 1:
            empty_x.append(i)

    for j in range(len(lines[0])):
        is_galaxy = False
        for i in range(len(lines)):
            if lines[i][j] == "#":
                is_galaxy = True
                break
        if not is_galaxy:
            empty_y.append(j)

    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "#":
                coordinates.append([i, j])

    distances_2 = []
    distances_1000000 = []
    for i in range(len(coordinates) - 1):
        for j in range(i + 1, len(coordinates)):
            distances_2.append(galaxy_distance(coordinates[i], coordinates[j], empty_x, empty_y, 2))
            distances_1000000.append(galaxy_distance(coordinates[i], coordinates[j], empty_x, empty_y, 1000000))

    return sum(distances_2), sum(distances_1000000)


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Tasks: {}'.format(task1_2(path)))
