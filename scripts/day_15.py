import time

DIRS = {
    '>': 1,
    '<': -1,
    '^': -1j,
    'v': 1j,
}

EXPAND_MAP = {
    '#': '##',
    'O': '[]',
    '.': '..',
    '@': '@.',
}

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        raw_data = f.read()

    grid, walk = raw_data.split('\n\n')
    walk = list(''.join(walk.split('\n')))
    grid = [[c for c in line] for line in grid.split('\n')]
    return grid, walk

def parse_grid(grid):
    character_loc = None
    rval_dict = dict()
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            pos = x+y*1j
            if char == '@':
                character_loc = pos
                char = '.'
            rval_dict[pos] = char
    return rval_dict, character_loc

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

def do_step(arena, loc, step):
    direc = DIRS[step]
    if arena[loc+direc] == '.':
        return arena, loc+direc
    if arena[loc+direc] == '#':
        return arena, loc

    # Must be O
    pointer = loc+direc
    while arena[pointer] == 'O':
        pointer += direc
    if arena[pointer] == '#':
        return arena, loc

    # Can move all circles
    arena[loc+direc] = '.'
    arena[pointer] = 'O'
    loc += direc
    return arena, loc

def get_checksum(arena):
    rval = 0
    for k, v in arena.items():
        if v not in '[O':
            continue
        x = int(k.real)
        y = int(k.imag)
        rval += 100*y + x
    return rval

def expand_grid(grid):
    return [list(''.join([EXPAND_MAP[c] for c in line])) for line in grid]

def do_step_v2(arena, loc, step):
    direc = DIRS[step]
    if arena[loc+direc] == '.':
        return arena, loc+direc
    if arena[loc+direc] == '#':
        return arena, loc

    # Must be []
    nodes = set()
    to_check = {loc+direc}
    can_move = True
    while len(to_check):
        current_node = to_check.pop()
        if current_node in nodes:
            continue
        current_symbol = arena[current_node]
        if current_symbol == '#':
            can_move = False
            break
        elif current_symbol == '.':
            continue
        elif current_symbol == ']':
            to_check.add(current_node+DIRS['<'])
            to_check.add(current_node+direc)
            nodes.add(current_node)
        elif current_symbol == '[':
            to_check.add(current_node+DIRS['>'])
            to_check.add(current_node+direc)
            nodes.add(current_node)
    if not can_move:
        return arena, loc

    new_k_v_pairs = []
    for node in nodes:
        k = node+direc
        v = arena[node]
        new_k_v_pairs.append((k, v))
    for node in nodes:
        arena[node] = '.'
    for k, v in new_k_v_pairs:
        arena[k] = v
    loc = loc+direc
    return arena, loc

# Main #
if __name__ == "__main__":
    grid, walk = load_data('data/day_15.dat')
    arena, loc = parse_grid(grid)

    # Part 1
    for step in walk:
        arena, loc = do_step(arena, loc, step)

    checksum_1 = get_checksum(arena)
    print(f"Part 1: {checksum_1}")

    # Visualise it!
    #show_arena(arena, loc)
    #time.sleep(0.25)
    #for step in walk:
    #    arena, loc = do_step(arena, loc, step)
    #    show_arena(arena, loc)
    #    time.sleep(0.25)

    # Part 2
    expanded_grid = expand_grid(grid)
    expanded_arena, expanded_loc = parse_grid(expanded_grid)

    for step in walk:
        expanded_arena, expanded_loc = do_step_v2(expanded_arena, expanded_loc, step)

    checksum_2 = get_checksum(expanded_arena)
    print(f"Part 2: {checksum_2}")

    # Visualise it!
    #show_arena(expanded_arena, expanded_loc)
    #time.sleep(0.001)
    #for step in walk:
        #expanded_arena, expanded_loc = do_step_v2(expanded_arena, expanded_loc, step)
        #show_arena(expanded_arena, expanded_loc)
        #time.sleep(0.001)
