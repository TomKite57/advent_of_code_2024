from collections import defaultdict
from itertools import combinations
from functools import reduce
from math import gcd

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [[x for x in l.strip()] for l in f.readlines()]

def grid_to_cmp_dicts(arr):
    coord_to_val = dict()
    val_to_coords = defaultdict(set)
    for y, row in enumerate(arr[::-1]):
        for x, v in enumerate(row):
            coord_to_val[x+y*1.j] = v
            val_to_coords[v].add(x+y*1.j)
    return coord_to_val, val_to_coords

def antinode_calculation(p1, p2):
    return 2*p1-p2, 2*p2-p1

def resonant_antinode_calculation(p1, p2, c_to_v):
    diff = p2-p1
    divisor = gcd(int(diff.real), int(diff.imag))
    if divisor != 1:
        diff //= divisor

    rval = set([p1])
    i = 1
    while True:
        pp, pm, i = p1+diff*i, p1-diff*i, i+1
        ps = {p for p in [pp, pm] if p in c_to_v}
        if not len(ps):
            return rval
        rval |= ps

def get_antinodes_of_char(map_obj, char, part):
    assert part in [1, 2]
    c_to_v, v_to_c = map_obj
    char_locs = v_to_c[char]
    if part==1:
        return {l for p in combinations(char_locs, 2) for l in antinode_calculation(*p) if l in c_to_v}
    return {l for p in combinations(char_locs, 2) for l in resonant_antinode_calculation(*p, c_to_v)}

# Main #
if __name__ == "__main__":
    data = load_data('data/day_08.dat')
    c_to_v, v_to_c = grid_to_cmp_dicts(data)
    map_tuple = (c_to_v, v_to_c)
    all_chars = [v for v in v_to_c.keys() if v != '.']

    antinodes = reduce(
        lambda a, b: a | b,
        [get_antinodes_of_char(map_tuple, c, part=1) for c in all_chars]
        )
    print(f"Part 1: {len(antinodes)}")

    antinodes = reduce(
        lambda a, b: a | b,
        [get_antinodes_of_char(map_tuple, c, part=2) for c in all_chars]
        )
    print(f"Part 2: {len(antinodes)}")