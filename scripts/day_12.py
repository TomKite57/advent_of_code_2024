DIRS = [
    +1+0.j,
    -1+0.j,
    +0+1.j,
    +0-1.j,
]

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [[c for c in line.strip()] for line in f.readlines()]

def map_to_dict(arr):
    rval = dict()
    for y, row in enumerate(arr[::-1]):
        for x, val in enumerate(row):
            rval[x+y*1.j] = val
    return rval

def explore_current_island(map_dict, loc):
    char = map_dict[loc]
    rval = set()
    rval.add(loc)
    path = [loc]
    while len(path):
        l = path.pop()
        for d in DIRS:
            nl = l+d
            if nl not in rval and nl in map_dict and map_dict[nl] == char:
                path.append(nl)
                rval.add(nl)
    return rval

def get_islands(map_dict):
    seen = set()
    islands = []
    for loc in map_dict.keys():
        if loc not in seen:
            new_island = explore_current_island(map_dict, loc)
            seen |= new_island
            islands.append(new_island)
    return islands

def island_checksum_p1(island):
    area = len(island)
    perim = 0
    for l in island:
        for d in DIRS:
            nl = d+l
            if nl not in island:
                perim += 1
    return area*perim


def walk_single_edge(edge_set, loc_dir):
    path = [loc_dir]
    rval = set()
    rval.add(loc_dir)
    while len(path):
        l, _d = path.pop()
        for d in DIRS:
            nl = l+d
            if (nl, _d) not in rval and (nl, _d) in edge_set:
                path.append((nl, _d))
                rval.add((nl, _d))
    return rval

def get_edges(island):
    ext_points = set()
    for l in island:
        for d in DIRS:
            nl = d+l
            if nl not in island:
                ext_points.add((nl, d))

    # Now cluster those points
    seen = set()
    edges = []
    for loc_dir in ext_points:
        if loc_dir in seen:
            continue
        new_edge = walk_single_edge(ext_points, loc_dir)
        seen |= new_edge
        edges.append(new_edge)

    return edges


def island_checksum_p2(island):
    area = len(island)
    edges = len(get_edges(island))
    return area*edges


# Main #
if __name__ == "__main__":
    data = load_data('data/day_12.dat')
    map_dict = map_to_dict(data)

    islands = get_islands(map_dict)
    checksum = sum((island_checksum_p1(i) for i in islands))
    print(f"Part 1: {checksum}")

    checksum = sum((island_checksum_p2(i) for i in islands))
    print(f"Part 2: {checksum}")
