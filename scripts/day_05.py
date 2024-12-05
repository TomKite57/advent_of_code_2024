from collections import defaultdict

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        data = f.read()

    rules, updates = data.strip().split('\n\n')
    rules = [[int(x) for x in l.strip().split('|')] for l in rules.split('\n')]
    updates = [[int(x) for x in l.strip().split(',')] for l in updates.split('\n')]

    return rules, updates

def valid_update(update, rule_dict):
    u_dict = {n: i for i, n in enumerate(update)}
    for i, n1 in enumerate(update):
        all_n2 = rule_dict[n1]
        for n2 in all_n2:
            if n2 in u_dict and u_dict[n2] < i:
                return False
    return True

def correct_update(update, rule_dict):
    if not update:
        return []

    # Find head
    for i, head in enumerate(update):
        found_problem = False
        for j, n in enumerate(update):
            if i == j:
                continue
            to_avoid = rule_dict[n]
            if head in to_avoid:
                found_problem = True
                break
        if not found_problem:
            break

    return [head] + correct_update([u for u in update if u != head], rule_dict)

# Main #
if __name__ == "__main__":
    rules, updates = load_data('data/day_05.dat')

    rule_dict = defaultdict(set)
    for r1, r2 in rules:
        rule_dict[r1].add(r2)

    checksum = 0
    for u in updates:
        if valid_update(u, rule_dict):
            checksum += u[len(u)//2]
    print(f"Part 1: {checksum}")

    checksum = 0
    for u in updates:
        if not valid_update(u, rule_dict):
            new_update = correct_update(u, rule_dict)
            checksum += new_update[len(new_update)//2]
    print(f"Part 2: {checksum}")


