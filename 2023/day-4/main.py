import re
import sys


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    total_sum = 0

    for line in lines:
        [left, lottery_numbers_string] = line.split("|")
        [card_name, winning_numbers_string] = left.split(': ')
        winning_numbers = [int(number) for number in winning_numbers_string.strip().split()]
        lottery_numbers = set([int(number) for number in lottery_numbers_string.strip().split()])

        winners = 0
        for number in winning_numbers:
            if number in lottery_numbers:
                winners = winners + 1

        if winners:
            total_sum = total_sum + 2 ** (winners - 1)

    return total_sum


def task2(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip() for line in file if line != '']

    total_sum = 0

    multipliers = [0 for line in lines]

    for index, line in enumerate(lines):
        [left, lottery_numbers_string] = line.split("|")
        [card_name, winning_numbers_string] = left.split(': ')
        winning_numbers = [int(number) for number in winning_numbers_string.strip().split()]
        lottery_numbers = set([int(number) for number in lottery_numbers_string.strip().split()])

        winners = 0
        for number in winning_numbers:
            if number in lottery_numbers:
                winners = winners + 1

        if winners:
            for i in range(winners):
                if i + index < len(multipliers):
                    multipliers[i + index + 1] = multipliers[i + index + 1] + multipliers[index] + 1

        total_sum = total_sum + multipliers[index] + 1

    return total_sum


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2(path)))
