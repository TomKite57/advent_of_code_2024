from collections import defaultdict

ARENA_MIN = 0
ARENA_MAX = 70

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [[int(x) for x in l.split(',')] for l in f.readlines()]

def coords_to_pos(x, y):
    return x + y*1j

def build_arena(x_lims, y_lims, do_pad=False):
    rval = defaultdict(lambda: '#')
    x_min, x_max = x_lims
    y_min, y_max = y_lims
    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            pos = coords_to_pos(x, y)
            rval[pos] = '.'

    if do_pad:
        rval[x_min-1 + (y_min-1)*1j]
        rval[x_max+1 + (y_max+1)*1j]
    return rval

def fill_arena(arena, chunks):
    for (x, y) in chunks:
        pos = coords_to_pos(x, y)
        arena[pos] = '#'
    return arena

def shortest_path(arena, start, end):
    paths = [(start, 0)]
    history = dict()

    while len(paths):
        current_pos, current_length = paths.pop()
        if current_pos in history and history[current_pos] <= current_length:
            continue
        history[current_pos] = current_length

        for step in [1, -1, 1j, -1j]:
            new_pos = current_pos + step
            if arena[new_pos] == '.':
                paths.append((new_pos, current_length+1))

    return history.get(end, -1)

def show_arena(arena, loc=None):
    xmin = min([int(x.real) for x in arena.keys()])
    xmax = max([int(x.real) for x in arena.keys()])
    ymin = min([int(x.imag) for x in arena.keys()])
    ymax = max([int(x.imag) for x in arena.keys()])

    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            pos = x+y*1j
            if loc is not None and loc==pos:
                print('@', end='')
            else:
                print(arena[pos], end='')
        print()

# Main #
if __name__ == "__main__":
    data = load_data('data/day_18.dat')
    start, end = coords_to_pos(ARENA_MIN, ARENA_MIN), coords_to_pos(ARENA_MAX, ARENA_MAX)

    kb_arena = build_arena([ARENA_MIN, ARENA_MAX], [ARENA_MIN, ARENA_MAX])
    kb_arena = fill_arena(kb_arena, data[:1024])
    checksum_1 = shortest_path(kb_arena, start, end)
    print(f"Part 1: {checksum_1}")

    for i in range(len(data)-1, -1, -1):
        arena = build_arena([ARENA_MIN, ARENA_MAX], [ARENA_MIN, ARENA_MAX])
        arena = fill_arena(arena, data[:i])
        path_len = shortest_path(arena, start, end)
        if path_len != -1:
            print(f"Part 2: {','.join(map(str, data[i]))}")
            break
