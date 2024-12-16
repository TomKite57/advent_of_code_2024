DIR_MAP = {
    '>': 1,
    '<': -1,
    '^': -1j,
    'v': 1j,
}
TURNS = {
    '>': '^v',
    '<': '^v',
    '^': '<>',
    'v': '<>',
}

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        grid = [[c for c in l.strip()] for l in f.readlines()]

    arena = dict()
    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            pos = x+y*1j
            arena[pos] = v

    return arena

def binary_insert(arr, elem, func):
    if len(arr) == 0:
        arr.append(elem)
        return
    if len(arr) == 1:
        if func(elem) > func(arr[0]):
            arr.append(elem)
        else:
            arr.insert(0, elem)
        return

    left, right = 0, len(arr)-1
    l_func, r_func = func(arr[left]), func(arr[right])
    e_func = func(elem)
    if r_func < e_func:
        arr.append(elem)
        return
    if l_func > e_func:
        arr.insert(0, elem)
        return

    while left <= right:
        mid = (left+right)//2
        m_func = func(arr[mid])
        if m_func == e_func:
            arr.insert(mid, elem)
            return
        if m_func < e_func:
            left = mid+1
            l_func = func(arr[left])
        else:
            right = mid-1
            r_func = func(arr[right])
    arr.insert(left, elem)

def walk_arena(arena):
    start_pos = None
    end_pos = None
    for k, v in arena.items():
        if v=='S':
            start_pos = k
        if v=='E':
            end_pos = k

    def heuristic(entry, end_pos=end_pos):
        path, direc, length = entry
        pos = path[-1]
        rval = 100*(abs(pos.real-end_pos.real) + abs(pos.imag-end_pos.imag)) + length
        return -rval

    best_dists = dict()
    paths = [([start_pos], '>', 0)]
    best_path_length = float("inf")
    saved_paths = []

    while len(paths):
        path, direc, length = paths.pop()
        pos = path[-1]

        if pos == end_pos:
            if length < best_path_length:
                best_path_length = min(best_path_length, length)
                saved_paths = [path]
            elif length == best_path_length:
                saved_paths.append(path)

        if length >= best_path_length:
            continue
        if best_dists.get((pos, direc), float('inf')) < length:
            continue
        best_dists[(pos, direc)] = length

        for d in TURNS[direc]:
            if arena.get(pos+DIR_MAP[d], '#') != '#':
                new_path = [p for p in path]
                new_path.append(pos+DIR_MAP[d])
                binary_insert(paths, (new_path, d, length+1+1000), heuristic)

        if arena.get(pos+DIR_MAP[direc], '#') != '#':
            new_path = [p for p in path]
            new_path.append(pos+DIR_MAP[direc])
            binary_insert(paths, (new_path, direc, length+1), heuristic)

    # Count seats
    best_path_points = set()
    for path in saved_paths:
        for pos in path:
            best_path_points.add(pos)

    return best_path_length, len(best_path_points)


# Main #
if __name__ == "__main__":
    data = load_data('data/day_16.dat')

    checksum_1, checksum_2 = walk_arena(data)

    print(f"Part 1: {checksum_1}")
    print(f"Part 2: {checksum_2}")

