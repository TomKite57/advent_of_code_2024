ROT_DIREC = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}
DIRECS = list(ROT_DIREC.keys())
FREE = set('.^<>v')
BLOCK = set('#')

def move_loc(loc, direc):
    return (loc[0]+direc[0], loc[1]+direc[1])

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        arr_data = [[c for c in l.strip()] for l in f.readlines()]
    dict_data = dict()
    for y, row in enumerate(arr_data[::-1]):
        for x, c in enumerate(row):
            dict_data[(x, y)] = c
    return dict_data


def initial_guard_walk(map_dict, loc, direc):
    seen = set([loc])
    while True:
        new_loc = move_loc(loc, direc)
        if new_loc not in map_dict:
            break
        if map_dict[new_loc] in FREE:
            loc = new_loc
            seen.add(loc)
        else:
            direc = ROT_DIREC[direc]

    return seen


def end_in_loop(map_dict, loc, direc, obstacle_loc):
    map_dict[obstacle_loc] = '#'

    seen = set([(loc, direc)])
    loop = None
    while True:
        new_loc = move_loc(loc, direc)
        if new_loc not in map_dict:
            loop = False
            break
        if (new_loc, direc) in seen:
            loop = True
            break
        if map_dict[new_loc] in FREE:
            loc = new_loc
            seen.add((loc, direc))
        else:
            direc = ROT_DIREC[direc]

    map_dict[obstacle_loc] = '.'

    return loop


# Main #
if __name__ == "__main__":
    data = load_data('data/day_06.dat')
    loc = [c for c, v in data.items() if v in '^<>v'][0]
    initial_walk = initial_guard_walk(data, loc, (0, 1))

    checksum = len(initial_walk)
    print(f"Part 1: {checksum}")

    checksum_2 = 0
    for o_loc in initial_walk:
        if o_loc == loc:
            continue
        if end_in_loop(data, loc, (0, 1), o_loc):
            checksum_2 += 1
    print(f"Part 2: {checksum_2}")
    # Not 5124



