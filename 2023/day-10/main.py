from pprint import pprint
import sys
from enum import Enum

START_POINT = "S"


class Directions(Enum):
    VERTICAL = 1
    HORIZONTAL = 2
    NORTH_WEST = 3
    NORTH_EAST = 4
    SOUTH_WEST = 5
    SOUTH_EAST = 6
    ALL = 7


SYMBOLS_MAP = {
    "|": Directions.VERTICAL,
    "-": Directions.HORIZONTAL,
    "J": Directions.NORTH_WEST,
    "L": Directions.NORTH_EAST,
    "7": Directions.SOUTH_WEST,
    "F": Directions.SOUTH_EAST,
    "S": Directions.ALL,
    ".": None
}

SYMBOLS_SCALING_MAP = {
    "|": [[' ', '*', ' '],
          [' ', '*', ' '],
          [' ', '*', ' ']],
    "-": [[' ', ' ', ' '],
          ['*', '*', '*'],
          [' ', ' ', ' ']],
    "J": [[' ', '*', ' '],
          ['*', '*', ' '],
          [' ', ' ', ' ']],
    "L": [[' ', '*', ' '],
          [' ', '*', '*'],
          [' ', ' ', ' ']],
    "7": [[' ', ' ', ' '],
          ['*', '*', ' '],
          [' ', '*', ' ']],
    "F": [[' ', ' ', ' '],
          [' ', '*', '*'],
          [' ', '*', ' ']],
    ".": [[' ', ' ', ' '],
          [' ', '.', ' '],
          [' ', ' ', ' ']]
}

ALL = "all"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

MOVES_INCREMENT = {
    UP: [-1, 0],
    DOWN: [1, 0],
    LEFT: [0, -1],
    RIGHT: [0, 1]
}

DIRECTIONS_MAP = {
    Directions.VERTICAL: [UP, DOWN],
    Directions.HORIZONTAL: [LEFT, RIGHT],
    Directions.NORTH_WEST: [LEFT, UP],
    Directions.NORTH_EAST: [RIGHT, UP],
    Directions.SOUTH_WEST: [LEFT, DOWN],
    Directions.SOUTH_EAST: [RIGHT, DOWN]
}


def get_moves(lines, x, y):
    allowed_directions = get_allowed_directions(lines, x, y)

    target_allowed = validate_destination(lines, x, y, allowed_directions)

    return target_allowed


def validate_destination(lines, x, y, validate_directions):
    valid_directions = []
    for direction in validate_directions:
        if direction == UP and DOWN in get_allowed_directions(lines, x - 1, y):
            valid_directions.append(UP)
        elif direction == DOWN and UP in get_allowed_directions(lines, x + 1, y):
            valid_directions.append(DOWN)
        elif direction == LEFT and RIGHT in get_allowed_directions(lines, x, y - 1):
            valid_directions.append(LEFT)
        elif direction == RIGHT and LEFT in get_allowed_directions(lines, x, y + 1):
            valid_directions.append(RIGHT)

    return valid_directions


def get_allowed_directions(lines, x, y):
    current_direction = SYMBOLS_MAP[lines[x][y]]

    if not current_direction:
        return []

    if current_direction == Directions.ALL:
        return [UP, LEFT, RIGHT, DOWN]

    return DIRECTIONS_MAP[current_direction]


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [[*line.strip()] for line in file if line != '']

    start_x = None
    start_y = None
    distances = []
    for x, line in enumerate(lines):
        x_line = []
        for y, symbol in enumerate(line):
            x_line.append(-1)
            if symbol == START_POINT:
                start_x = x
                start_y = y
        distances.append(x_line)

    print(start_x, start_y)

    distances[27][32] = 0
    active_paths = [[27, 32]]
    max_distance = 0

    while len(active_paths):
        [x, y] = active_paths.pop(0)

        moves = get_moves(lines, x, y)

        for move in moves:
            move_increment = MOVES_INCREMENT[move]
            current_target_distance = distances[x + move_increment[0]][y + move_increment[1]]

            if current_target_distance == -1:
                active_paths.append([x + move_increment[0], y + move_increment[1]])
                new_distance = distances[x][y] + 1
                distances[x + move_increment[0]][y + move_increment[1]] = new_distance

                if new_distance > max_distance:
                    max_distance = new_distance

    active = [[0, 0]]
    visited = {}

    while len(active):
        [x, y] = active.pop()
        if x < 0 or y < 0 or x >= len(lines) or y >= len(lines[0]) or distances[x][y] != -1 or visited.get(f"{x}_{y}"):
            continue

        visited[f"{x}_{y}"] = True
        lines[x][y] = " "
        active.append([x + 1, y])
        active.append([x - 1, y])
        active.append([x, y + 1])
        active.append([x, y - 1])

    scaled_lines = []
    for i in range(len(lines) * 3):
        scaled_line = []
        for j in range(len(lines[0]) * 3):
            scaled_line.append(" ")
        scaled_lines.append(scaled_line)

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            scaled_map = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
            if SYMBOLS_SCALING_MAP.get(lines[i][j]) and distances[i][j] != -1:
                scaled_map = SYMBOLS_SCALING_MAP[lines[i][j]]

            for ii in range(len(scaled_map)):
                for jj in range(len(scaled_map[0])):
                    scaled_lines[i * 3 + ii][j * 3 + jj] = scaled_map[ii][jj]
                    if ii == jj == 1 and distances[i][j] == -1:
                        scaled_lines[i * 3 + ii][j * 3 + jj] = lines[i][j]

    with open("results.txt", "w") as write_file:
        write_file.writelines(["".join(line + ["\n"]) for line in scaled_lines])

    return max_distance


def task2():
    file = open("results.txt", "r")
    lines = [[*line.strip("")] for line in file]

    active = [[0, 0]]
    visited = {}

    while len(active):
        [x, y] = active.pop()
        if x < 0 or y < 0 or x >= len(lines) or y >= len(lines[0]) or lines[x][y] == "*" or visited.get(f"{x}_{y}"):
            continue

        visited[f"{x}_{y}"] = True
        lines[x][y] = " "
        active.append([x + 1, y])
        active.append([x - 1, y])
        active.append([x, y + 1])
        active.append([x, y - 1])

    with open("results_cleaned.txt", "w") as write_file:
        write_file.writelines(["".join(line + ["\n"]) for line in lines])

    dots_count = 0
    for line in lines:
        for symbol in line:
            if symbol != " " and symbol != "*":
                dots_count = dots_count + 1

    return dots_count


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2()))
