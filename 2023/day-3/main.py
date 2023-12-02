import re
import sys


def process_lines(lines: list[str]):
    games = []

    for line in lines:
        [game_id_string, games_string] = line.split(':')
        games_list = [game.split(',') for game in games_string.split(';')]

        games_iteration = []
        for games_list in games_list:
            game = {}
            for ball in games_list:
                [value, name] = ball.strip().split(' ')
                if not game.get(name):
                    game[name] = int(value)
                else:
                    game[name] = game[name] + int(value)
            games_iteration.append(game)
        games.append(games_iteration)

    return games


def check_balls(game_subset: dict, key, value):
    return game_subset.get(key) and game_subset.get(key) > value


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    data = process_lines(lines)

    print(data)

    possible_games = []
    for i, game in enumerate(data):
        success = True
        for subset in game:
            if (check_balls(subset, "red", 12)
                    or check_balls(subset, "green", 13)
                    or check_balls(subset, "blue", 14)):
                success = False
                break

        if success:
            possible_games.append(i + 1)

    return sum(possible_games)


def task2(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    data = process_lines(lines)

    games_power = []
    colors = ["red", "green", "blue"]
    for i, game in enumerate(data):
        max_values = {}
        for subset in game:
            for color in colors:
                if subset.get(color):
                    if not max_values.get(color):
                        max_values[color] = subset[color]
                    elif max_values[color] < subset[color]:
                        max_values[color] = subset[color]

        power = 1
        for color in colors:
            if max_values.get(color):
                power = power * max_values[color]

        games_power.append(power)

    return sum(games_power)


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    # print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2(path)))
