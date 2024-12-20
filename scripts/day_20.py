# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [[c for c in line.strip()] for line in f.readlines()]

def manhattan_comp(z):
    return abs(z.real) + abs(z.imag)

def maze_to_dict(maze):
    rval = dict()
    start, end = None, None
    for y, row in enumerate(maze):
        for x, c in enumerate(row):
            p = x+y*1j
            if c == "S":
                start = p
                c = '.'
            if c == "E":
                end = p
                c = '.'
            rval[p] = c
    return rval, start, end

def get_dist_from_node(maze, start, node):
    paths = [(node, 0)]
    history = dict()

    while len(paths):
        pos, length = paths.pop()

        if pos in history and history[pos] <= length:
            continue
        history[pos] = length

        for step in [1, -1, 1j, -1j]:
            new_pos = pos + step
            if maze.get(new_pos) != '.':
                continue
            paths.append((new_pos, length+1))

    return history

def find_single_cheat_paths(maze, start, end, cutoff=100):
    total_count = 0
    dist_from_end = get_dist_from_node(maze, start, end)
    dist_from_start = get_dist_from_node(maze, start, start)
    shortest_path = dist_from_end[start]

    for k, v in maze.items():
        if v !='#':
            continue

        s_dists, e_dists = [], []
        for step in [1, -1, 1j, -1j]:
            p = k+step
            if p in dist_from_end:
                e_dists.append(dist_from_end[p])
            if p in dist_from_start:
                s_dists.append(dist_from_start[p])
        if len(s_dists) == 0 or len(e_dists) == 0:
            continue

        path_length = min(s_dists) + min(e_dists) + 2
        advantage = shortest_path - path_length
        if advantage >= cutoff:
            total_count += 1

    return total_count


def this_took_me_so_long_oh_my_god(maze, start, end, cutoff=100, max_cheats=20):
    dist_from_end = get_dist_from_node(maze, start, end)
    dist_from_start = get_dist_from_node(maze, start, start)
    shortest_path = dist_from_end[start]

    cheats = dict()

    for s_pos, s_char in maze.items():
        if s_char == '#':
            continue
        if s_pos not in dist_from_start:
            continue
        start_to_s = dist_from_start[s_pos]
        if shortest_path - start_to_s - manhattan_comp(end-s_pos) < cutoff:
            continue

        for e_pos, e_char in maze.items():
            if e_char == '#':
                continue
            if e_pos not in dist_from_end:
                continue
            cheat_travel = int(manhattan_comp(e_pos-s_pos))
            if cheat_travel > max_cheats:
                continue
            e_to_end = dist_from_end[e_pos]
            advantage = shortest_path - (start_to_s + cheat_travel + e_to_end)
            if advantage >= cutoff:
                cheats[(s_pos, e_pos)] = advantage

    return len(cheats)


# Main #
if __name__ == "__main__":
    data = load_data('data/day_20.dat')
    maze, start, end = maze_to_dict(data)

    checksum_1 = find_single_cheat_paths(maze, start, end, 100)
    print(f"Part 1: {checksum_1}")

    checksum_2 = this_took_me_so_long_oh_my_god(maze, start, end, 100, 20)
    print(f"Part 2: {checksum_2}")

