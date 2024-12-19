from functools import cache

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        towels, patterns = f.read().split('\n\n')

    towels = tuple(towels.strip().split(', '))
    patterns = patterns.strip().split('\n')

    return towels, patterns

@cache
def count_pattern_options(pattern, towels):
    count = 0

    for t in towels:
        lt = len(t)
        if lt > len(pattern):
            continue
        if pattern[:lt] == t:
            if lt == len(pattern):
                count += 1
            else:
                count += count_pattern_options(pattern[lt:], towels)

    return count


# Main #
if __name__ == "__main__":
    towels, patterns = load_data('data/day_19.dat')
    pattern_counts = [count_pattern_options(p, towels) for p in patterns]

    checksum_1 = sum([int(bool(x)) for x in pattern_counts])
    print(f"Part 1: {checksum_1}")

    checksum_2 = sum(pattern_counts)
    print(f"Part 2: {checksum_2}")