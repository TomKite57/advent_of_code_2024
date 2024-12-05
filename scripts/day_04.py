import itertools

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [[x for x in l.strip()] for l in f.readlines()]

def get_char_locations(data, char):
    rval = []
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c==char:
                rval.append((i, j))
    return rval


# Part 1 #
def count_words_at_loc(data, word, loc):
    rval = 0
    i, j = loc
    n = len(word)

    for di, dj in itertools.product([-1, 0, 1], [-1, 0, 1]):
        if di == dj == 0:
            continue

        test = []
        for k in range(n):
            ii, jj = i+k*di, j+k*dj
            if (not 0 <= ii < len(data)) or (not 0 <= jj < len(data[0])):
                break
            test.append(data[ii][jj])
        if len(test) == n and "".join(test) == word:
            rval += 1

    return rval

def count_words_at_al_locs(data, word):
    locs = get_char_locations(data, word[0])
    return sum((count_words_at_loc(data, word, l) for l in locs))


# Part 2 #
def is_cross(data, loc):
    i, j = loc
    im1, ip1, jm1, jp1 = i-1, i+1, j-1, j+1
    if im1 < 0 or ip1 >= len(data) or jm1 < 0 or jp1 >= len(data[0]):
        return 0

    d1 = set([data[im1][jm1], data[ip1][jp1]])
    d2 = set([data[im1][jp1], data[ip1][jm1]])
    return int(d1 == d2 == set('MS'))

def count_all_crosses(data):
    locs = get_char_locations(data, 'A')
    return sum((is_cross(data, l) for l in locs))


# Main #
if __name__ == "__main__":
    data = load_data('data/day_04.dat')

    checksum = count_words_at_al_locs(data, 'XMAS')
    print(f"Part 1: {checksum}")

    checksum = count_all_crosses(data)
    print(f"Part 2: {checksum}")
