import re
import sys


def calc_win_races(grouped_races):
    acceleration = 1
    races_wins = []
    for [time, distance] in grouped_races:
        race_wins = []

        for t in range(time):
            traveled_distance = acceleration * t * (time - t)
            if traveled_distance > distance:
                race_wins.append([t, traveled_distance])

        races_wins.append(len(race_wins))

    return races_wins


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    seconds = [int(value) for value in lines[0].split()]
    distances = [int(value) for value in lines[1].split()]

    grouped_races = list(zip(seconds, distances))

    races_wins = calc_win_races(grouped_races)

    total_mul = 1
    for value in races_wins:
        total_mul = total_mul * value

    return total_mul


def task2(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    seconds = int(lines[0].strip().replace(" ", ""))
    distances = int(lines[1].strip().replace(" ", ""))

    races_wins = calc_win_races([[seconds, distances]])

    total_mul = 1
    for value in races_wins:
        total_mul = total_mul * value

    return total_mul


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2(path)))
