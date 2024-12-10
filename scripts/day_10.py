DIRS = [
    +1+0.j,
    -1+0.j,
    +0+1.j,
    +0-1.j,
]

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [[int(x) for x in l.strip()] for l in f.readlines()]

def map_to_dict(arr):
    rval = dict()
    for y, row in enumerate(arr[::-1]):
        for x, val in enumerate(row):
            rval[x+y*1.j] = val
    return rval

def get_starting_locs(map_dict):
    return [k for k, v in map_dict.items() if v==0]

def get_trail_degree(map_dict, loc):
    paths = [loc]
    final_locs = set()
    path_count = 0

    while len(paths):
        current = paths.pop()
        height = map_dict[current]
        if height == 9:
            final_locs.add(current)
            path_count += 1
            continue
        for direction in DIRS:
            new_loc = current+direction
            if new_loc in map_dict and map_dict[new_loc] == height+1:
                paths.append(new_loc)
    return len(final_locs), path_count


# Main #
if __name__ == "__main__":
    data = load_data('data/day_10.dat')
    map_dict = map_to_dict(data)
    start_locs = get_starting_locs(map_dict)

    checksum_1, checksum_2 = 0, 0
    for l in start_locs:
        c1, c2 = get_trail_degree(map_dict, l)
        checksum_1 += c1
        checksum_2 += c2
    print(f"Part 1: {checksum_1}")
    print(f"Part 2: {checksum_2}")