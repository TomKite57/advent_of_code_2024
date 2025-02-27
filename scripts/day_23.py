from collections import defaultdict

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [sorted(x.strip().split('-')) for x in f.readlines()]

def make_connection_map(data):
    rval = defaultdict(set)
    for a, b in data:
        rval[a].add(b)
        rval[b].add(a)
    return rval

def find_all_t_triples(connection_map):
    all_computers = set(connection_map.keys())

    all_t_computers = [x for x in all_computers if x[0]=='t']

    all_t_triples = set()
    for tc in all_t_computers:
        others = connection_map[tc]
        for o1 in others:
            other_others = connection_map[o1].intersection(others)
            for o2 in other_others:
                all_t_triples.add(frozenset(sorted([tc, o1, o2])))
    return all_t_triples

# Main #
if __name__ == "__main__":
    data = load_data('data/day_23.dat')
    connection_map = make_connection_map(data)

    all_t_triples = find_all_t_triples(connection_map)
    checksum_1 = len(all_t_triples)
    print(f"Part 1: {checksum_1}")

    groups = {k: tuple(sorted([k]+list(v))) for k, v in connection_map.items()}
    filtered_groups = []

    all_computers = sorted(list(connection_map.keys()))
    for c1 in all_computers:
        overlap_counts = defaultdict(int)
        for c2 in groups[c1]:
            overlap = set(groups[c1]).intersection(groups[c2])
            for i in range(len(overlap)+1):
                overlap_counts[i] += 1
        degrees = [k for k, v in overlap_counts.items() if k==v]
        if not degrees:
            continue
        degree_of_group = max(degrees)

        built_group = []
        for c2 in groups[c1]:
            overlap = set(groups[c1]).intersection(groups[c2])
            if len(overlap) >= degree_of_group:
                built_group.append(c2)
        filtered_groups.append(tuple(sorted(built_group)))

    counts = defaultdict(int)
    for g in filtered_groups:
        counts[len(g)] += 1
    counts = {k: v for k, v in counts.items() if k==v}
    for k, v in counts.items():
        lan_group_size = k

    lan_groups = [g for g in filtered_groups if len(g)==lan_group_size]
    lan_group = next(iter(set(lan_groups)))
    print(f"Part 2: {','.join(lan_group)}")


