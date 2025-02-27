# Helper functions #
SPACE = 6

def load_data(fname):
    with open(fname, 'r') as f:
        elements = [e.split('\n') for e in f.read().strip().split('\n\n')]

    keys, locks = [], []
    for elem in elements:
        is_key = '.' in elem[0]
        counts = [-1 for _ in elem[0]]
        for row in elem:
            for i, c in enumerate(row):
                counts[i] += int(c=='#')

        if is_key:
            keys.append(counts)
        else:
            locks.append(counts)

    return keys, locks

def does_it_fit(key, lock):
    for c1, c2 in zip(key, lock):
        if c1+c2 >= SPACE:
            return False
    return True

# Main #
if __name__ == "__main__":
    keys, locks = load_data('data/day_25.dat')

    checksum_1 = 0
    for k in keys:
        for l in locks:
            checksum_1 += int(does_it_fit(k, l))
    print(f"Part 1: {checksum_1}")