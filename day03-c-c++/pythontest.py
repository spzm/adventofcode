from collections import Counter

def part1(data, p):  # p=0 finds most common number, p=-1 finds least common
    return int(''.join([Counter(x).most_common()[p][0] for x in zip(*data)]), 2)

def part2(data, p):
    for n in range(12):
        counts = Counter(list(zip(*data))[n]).most_common()
        c = str(1 + p) if (len(counts) == 2 and counts[0][1] == counts[1][1]) else counts[p][0]
        data = list(filter(lambda x: x[n]==c, data))
    return int(''.join(data[0]), 2)

if __name__ == '__main__':
    with open('./data.txt') as f:
        data = [[bit for bit in bits] for bits in list(f.read().split())]

    print('power:', part1(data, 0) * part1(data, -1))
    print('life support: {0:b} {0:b}'.format(part2(data, 0), part2(data, -1)), part2(data, 0), part2(data, -1))