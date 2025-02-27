# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [int(x) for x in f.readlines()]

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216

def get_secrets(x, repeat=2000):
    rvals = [x]
    for _ in range(repeat):
        x = prune(mix(x*64, x))
        x = prune(mix(int(x/32), x))
        x = prune(mix(x*2048, x))
        rvals.append(x)
    return rvals

def get_subseq_loc(sequence, l=4):
    rval = dict()
    for i in range(1, len(sequence)-l+1):
        subseq = tuple(sequence[i:i+l])
        if subseq in rval:
            continue
        rval[subseq] = i+l-1
    return rval

# Main #
if __name__ == "__main__":
    data = load_data('data/day_22.dat')

    checksum_1 = sum((get_secrets(x)[-1] for x in data))
    print(f"Part 1: {checksum_1}")

    sequences = [get_secrets(x) for x in data]
    sequences = [[int(str(x)[-1]) for x in seq] for seq in sequences]
    changes = [[0] + [b-a for a, b in zip(s[:-1], s[1:])] for s in sequences]
    pattern_map = [get_subseq_loc(c) for c in changes]
    all_patterns = set()
    for p in pattern_map:
        all_patterns |= set(p.keys())

    max_p, total = None, 0
    for p in all_patterns:
        count = 0
        for s, c, pmap in zip(sequences, changes, pattern_map):
            if p not in pmap:
                continue
            count += s[pmap[p]]
        if count > total:
            max_p = p
            total = count
    print(f"Part 2: {total}")
