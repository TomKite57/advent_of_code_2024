from functools import cache
from collections import defaultdict

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [int(x) for x in f.read().strip().split(' ')]

@cache
def rule(stone):
    if stone == 0:
        return [1]

    ss = str(stone)
    if len(ss)%2 == 0:
        num = stone
        a, b = int(ss[:len(ss)//2]), int(ss[len(ss)//2:])
        return [a, b]

    return [stone*2024]

def update(stones):
    new_stones = defaultdict(int)

    for s, c in stones.items():
        for r in rule(s):
            new_stones[r] += c

    return new_stones


# Main #
if __name__ == "__main__":
    data = load_data('data/day_11.dat')
    data = {n: data.count(n) for n in data}

    for _ in range(25):
        data = update(data)
    print(f"Part 1: {sum(data.values())}")

    for _ in range(50):
        data = update(data)
    print(f"Part 2: {sum(data.values())}")
