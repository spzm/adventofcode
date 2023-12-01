import sys


def task1(file_name: str, window: int):
    file = open(file_name, 'r')
    previous_lines = [file.readline() for x in range(window)]

    return previous_lines


def task2(file_name: str, window: int):
    file = open(file_name, 'r')
    previous_lines = [file.readline() for x in range(window)]

    return previous_lines


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task: {}'.format(task1(path, 1)))
    print('3-measurement sliding window: {}\n'.format(task2(path, 3)))
