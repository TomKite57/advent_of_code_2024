

def load_data(fname):
    with open(fname, 'r') as f:
        return [[int(x) for x in l.strip().split(' ')] for l in f.readlines()]

def is_safe(line):
    if line[1] - line[0] == 0:
        return False

    inc = 1 if (line[1] - line[0]) > 0 else -1

    for a, b in zip(line[:-1], line[1:]):
        if not (0 < inc*(b-a) < 4):
            return False

    return True

def is_safe_with_tol(line):
    if is_safe(line):
        return True

    for i, _ in enumerate(line):
        new_line = line[:i] + line[i+1:]
        if is_safe(new_line):
            return True

    return False

if __name__ == "__main__":
    data = load_data('data/day_02.dat')

    num_safe = len([1 for l in data if is_safe(l)])
    print(f"Part 1: {num_safe}")

    num_safe = len([1 for l in data if is_safe_with_tol(l)])
    print(f"Part 2: {num_safe}")