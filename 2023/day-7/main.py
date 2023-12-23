import sys
from functools import cmp_to_key

strength = {"A": 13, "K": 12, "Q": 11, "J": 10, "T": 9, "9": 8, "8": 7, "7": 6, "6": 5, "5": 4, "4": 3, "3": 2, "2": 1}
strength_with_jocker = {"A": 13, "K": 12, "Q": 11, "J": 1, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4,
                        "3": 3, "2": 2}


def compare_by_symbol(cards1, cards2, strength_map):
    for symbol1, symbol2 in zip(cards1, cards2):
        if symbol1 != symbol2:
            return strength_map[symbol1] - strength_map[symbol2]

    return 0


def build_compare(to_map, strength_map):
    def compare(cards1, cards2):
        cards1_value = cards1[0]
        cards2_value = cards2[0]
        cards1_map = to_map(cards1_value)
        cards2_map = to_map(cards2_value)

        checks = [
            lambda card: card.get(5),
            lambda card: card.get(4),
            lambda card: card.get(3) and card.get(2),
            lambda card: card.get(3),
            lambda card: card.get(2) and len(card.get(2)) == 2,
            lambda card: card.get(2) and len(card.get(2)) == 1
        ]

        for check in checks:
            if check(cards1_map) or check(cards2_map):
                if check(cards1_map) and check(cards2_map):
                    return compare_by_symbol(cards1_value, cards2_value, strength_map)
                return 1 if check(cards1_map) else -1

        return compare_by_symbol(cards1_value, cards2_value, strength_map)

    return compare


def to_cards_map(cards):
    cards_map = {}
    for card in cards:
        if not cards_map.get(card):
            cards_map[card] = 1
        else:
            cards_map[card] = cards_map[card] + 1

    cards_reverse_map = {}
    for key, value in cards_map.items():
        if not cards_reverse_map.get(value):
            cards_reverse_map[value] = []
        cards_reverse_map[value].append(key)

    return cards_reverse_map


def to_cards_map_with_joker(cards):
    cards_map = {}
    jokers_count = cards.count("J")
    if jokers_count == 5:
        return {5: "J"}

    for card in cards:
        if card == "J":
            continue

        if not cards_map.get(card):
            cards_map[card] = 1
        else:
            cards_map[card] = cards_map[card] + 1

    max_card_key = max(cards_map, key=cards_map.get)
    cards_map[max_card_key] = cards_map[max_card_key] + jokers_count

    cards_reverse_map = {}
    for key, value in cards_map.items():
        if not cards_reverse_map.get(value):
            cards_reverse_map[value] = []
        cards_reverse_map[value].append(key)

    return cards_reverse_map


def task1(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip().split() for line in file if line != '']

    sorted_lines = sorted(lines, key=cmp_to_key(build_compare(to_cards_map, strength)))

    return sum([int(line[1]) * (i + 1) for i, line in enumerate(sorted_lines)])


def task2(file_name: str):
    file = open(file_name, "r")
    lines = [line.strip().split() for line in file if line != '']

    sorted_lines = sorted(lines, key=cmp_to_key(build_compare(to_cards_map_with_joker, strength_with_jocker)))

    return sum([int(line[1]) * (i + 1) for i, line in enumerate(sorted_lines)])


if __name__ == "__main__":
    path = sys.argv[1]

    if path is None:
        print('No file name provided')
        sys.exit()

    print('Processing results for path: {}'.format(path))
    print('Task 1: {}'.format(task1(path)))
    print('Task 2: {}'.format(task2(path)))
