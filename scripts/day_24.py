from numpy.random import choice

INPUT_BITS = 45
OUTPUT_BITS = 46

GATE_FUNCS = {
    'AND': lambda a, b : int(a and b),
    'OR': lambda a, b : int(a or b),
    'XOR': lambda a, b : int((a and not b) or (b and not a)),
}

# Helper functions #
def parse_wire(line):
    name, num = line.strip().split(': ')
    num = int(num)
    return name, num

def parse_gate(line):
    w1, g, w2, _, out = line.strip().split(' ')
    return [w1, g, w2, out]

def load_data(fname):
    with open(fname, 'r') as f:
        wires, gates = f.read().split('\n\n')

    wires = [parse_wire(w) for w in wires.split('\n')]
    wires = {a: b for a, b in wires}
    gates = [parse_gate(g) for g in gates.split('\n')]

    return wires, gates

def bin_to_int(x):
    return int(x, 2)

def int_to_bin(x, length=OUTPUT_BITS):
    rval = bin(x)[2:]
    l = len(rval)
    if l == length:
        return rval
    return ''.join(['0'*(length-l), rval])

def read_from_wires(wires, name='z', to_int=False):
    wire_names = sorted([w for w in wires.keys() if w.startswith(name)], reverse=True)
    string = ''.join([str(wires[w]) for w in wire_names])
    if to_int:
        return bin_to_int(string)
    return string

def solve_system(wire_dict, gates):
    wire_dict = wire_dict.copy()
    num_solved = len(wire_dict)

    while True:
        any_gate_left = False

        for w1, g, w2, out in gates:
            if out in wire_dict:
                continue

            if not (w1 in wire_dict and w2 in wire_dict):
                any_gate_left = True
                continue

            v1, v2 = wire_dict[w1], wire_dict[w2]
            v3 = GATE_FUNCS[g](v1, v2)
            wire_dict[out] = v3

        if len(wire_dict) == num_solved:
            return -1
        num_solved = len(wire_dict)

        if not any_gate_left:
            break

    return read_from_wires(wire_dict, 'z')

def get_random_wires():
    wires = dict()
    wires.update({f'x{i:>02}': choice([0, 1]) for i in range(INPUT_BITS)})
    wires.update({f'y{i:>02}': choice([0, 1]) for i in range(INPUT_BITS)})
    x, y = read_from_wires(wires, 'x', to_int=True), read_from_wires(wires, 'y', to_int=True)
    return wires, x, y

def string_print(iterable, sep=''):
    print(sep.join([str(x) for x in iterable]))

def get_col(matrix, i):
    return [row[i] for row in matrix]

def initial_sweep(gates):
    O, Z, C = [], [], []
    #for i in range(30_000):
    #for i in range(100_000):
    for i in range(5_000):
        wires, x, y = get_random_wires()
        z = x + y
        bz = int_to_bin(z, length=OUTPUT_BITS)
        out = solve_system(wires, gates)
        correct_bits = [int(i==j) for i, j in zip(bz, out)]

        Z.append(bz)
        O.append(out)
        C.append(correct_bits)

    correct_inds = []
    for a in range(len(C[0])-1, -1, -1):
        a_col = get_col(C, a)
        if all(a_col):
            correct_inds.append(OUTPUT_BITS-1-a)
    correct_inds = sorted(correct_inds)

    # Now look for two columns that are always 11 or 00
    swapped_inds = []
    for a in range(len(C[0])-1, -1, -1):
        for b in range(len(C[0])-1, -1, -1):
            if b<=a:
                continue
            if OUTPUT_BITS-1-a in correct_inds or OUTPUT_BITS-1-b in correct_inds:
                continue
            a_col, b_col = get_col(C, a), get_col(C, b)
            always_same = all([aa == bb for aa, bb in zip(a_col, b_col)])
            if always_same:
                swapped_inds.append((OUTPUT_BITS-1-a, OUTPUT_BITS-1-b))

    return list(correct_inds), list(swapped_inds)

def get_correct_gates_from_out_names(gates, out_names):
    correct_gates = set()
    correct_wires = set(out_names)
    num_correct = len(correct_wires)

    while True:
        for i, (w1, g, w2, out) in enumerate(gates):
            if out in correct_wires:
                correct_gates.add(i)
                correct_wires.add(w1)
                correct_wires.add(w2)
        if len(correct_wires) == num_correct:
            break
        num_correct = len(correct_wires)

    return sorted(list(correct_gates))

def get_children(gates, ind):
    children = set()
    to_check = [gates[ind][-1]]
    while len(to_check):
        current = to_check.pop()
        for i, (w1, g, w2, out) in enumerate(gates):
            if current in [w1, w2]:
                to_check.append(out)
                children.add(i)
    return children

def check_gates_correct(gates, tries=1_000):
    for i in range(tries):
        wires, x, y = get_random_wires()
        z = x + y
        bz = int_to_bin(z, length=OUTPUT_BITS)
        out = solve_system(wires, gates)
        if bz != out:
            return False
    return True

# Main #
if __name__ == "__main__":
    wires, initial_gates = load_data('data/day_24.dat')

    checksum_1 = bin_to_int(solve_system(wires, initial_gates))
    print(f"Part 1: {checksum_1}")

    #max_bit = max([int(w[1:]) for w in wires.keys() if w[0]=='x'])
    #x = int(''.join([str(wires[f"x{i:>02}"]) for i in range(max_bit+1)]), 2)
    #y = int(''.join([str(wires[f"y{i:>02}"]) for i in range(max_bit+1)]), 2)
    #z = checksum_1
    #print(x+y, z, x+y==z)

    # print("Round 1")
    # correct_z_bits, z_bits_to_swap = initial_sweep(initial_gates)
    # assert len(z_bits_to_swap) == 1
    # z_bits_to_swap = z_bits_to_swap[0]
    # actual_inds_to_swap = [None, None]
    # for i, (_, _, _, out) in enumerate(initial_gates):
    #     if out == f'z{z_bits_to_swap[0]:>02}':
    #         actual_inds_to_swap[0] = i
    #     if out == f'z{z_bits_to_swap[1]:>02}':
    #         actual_inds_to_swap[1] = i
    # print(f"{actual_inds_to_swap=}")

    # gates_with_one_swap = [g.copy() for g in initial_gates]
    # print(gates_with_one_swap[actual_inds_to_swap[0]], gates_with_one_swap[actual_inds_to_swap[1]])
    # gates_with_one_swap[actual_inds_to_swap[0]][-1], gates_with_one_swap[actual_inds_to_swap[1]][-1] = \
    #     gates_with_one_swap[actual_inds_to_swap[1]][-1], gates_with_one_swap[actual_inds_to_swap[0]][-1]
    # print(gates_with_one_swap[actual_inds_to_swap[0]], gates_with_one_swap[actual_inds_to_swap[1]])

    # print("Round 2")
    # correct_inds, swapped_inds = initial_sweep(gates_with_one_swap)

    #correct_z_bits, _ = initial_sweep(initial_gates)
    correct_z_bits = [0, 1, 2, 3, 4, 5, 6, 34] # Cached from a run with 100k samples
    correct_z_names = [f'z{bit:>02}' for bit in correct_z_bits]
    correct_gates = get_correct_gates_from_out_names(initial_gates, correct_z_names)

    incorrect_gates = [i for i in range(len(initial_gates)) if i not in correct_gates]

    children = [get_children(initial_gates, ind) for ind in incorrect_gates]
    children = [ch.intersection(set(incorrect_gates)) for ch in children]

    sort_inds = sorted([i for i in range(len(incorrect_gates))], key=lambda i: len(children[i]), reverse=True)
    incorrect_gates = [incorrect_gates[i] for i in sort_inds]
    children = [children[i] for i in sort_inds]

    #print(f"*{len(incorrect_gates)}*")
    #for i, ch in zip(incorrect_gates, children):
        #print(len(ch))

    for i1, ch1 in zip(incorrect_gates, children):
        for i2, ch2 in zip(incorrect_gates, children):
            if i2<=i1:
                continue
            if abs(len(ch1)-len(ch2)) > 5:
                continue
            new_gates = [g.copy() for g in initial_gates]
            new_gates[i1][-1], new_gates[i2][-1] = new_gates[i2][-1], new_gates[i1][-1]
            second_correct_z_bits, _ = initial_sweep(initial_gates)
            print(i1, i2, ':', len(correct_z_bits), len(second_correct_z_bits))

    # seen = set()
    # total_possible = len(incorrect_gates) * \
    #                 (len(incorrect_gates)-1) * \
    #                 (len(incorrect_gates)-2) * \
    #                 (len(incorrect_gates)-3) * \
    #                 (len(incorrect_gates)-4) * \
    #                 (len(incorrect_gates)-5) * \
    #                 (len(incorrect_gates)-6) * \
    #                 (len(incorrect_gates)-7)
    # finished = False
    # for ix1, (x1, chx1) in enumerate(zip(incorrect_gates, children)):
    #     if finished:
    #         break
    #     for ix2, (x2, chx2) in enumerate(zip(incorrect_gates, children)):
    #         if finished:
    #             break
    #         if ix2 in [ix1]:
    #             continue
    #         for iy1, (y1, chy1) in enumerate(zip(incorrect_gates, children)):
    #             if finished:
    #                 break
    #             if iy1 in [ix1, ix2]:
    #                 continue
    #             for iy2, (y2, chy2) in enumerate(zip(incorrect_gates, children)):
    #                 if finished:
    #                     break
    #                 if iy2 in [ix1, ix2, iy1]:
    #                     continue
    #                 for iz1, (z1, chz1) in enumerate(zip(incorrect_gates, children)):
    #                     if finished:
    #                         break
    #                     if iz1 in [ix1, ix2, iy1, iy2]:
    #                         continue
    #                     for iz2, (z2, chz2) in enumerate(zip(incorrect_gates, children)):
    #                         if finished:
    #                             break
    #                         if iz2 in [ix1, ix2, iy1, iy2, iz1]:
    #                             continue
    #                         for iw1, (w1, chw1) in enumerate(zip(incorrect_gates, children)):
    #                             if finished:
    #                                 break
    #                             if iw1 in [ix1, ix2, iy1, iy2, iz1, iz2]:
    #                                 continue
    #                             for iw2, (w2, chw2) in enumerate(zip(incorrect_gates, children)):
    #                                 if finished:
    #                                     break
    #                                 if iw2 in [ix1, ix2, iy1, iy2, iz1, iz2, iw1]:
    #                                     continue
    #                                 ch_sum = sum((len(c) for c in [chx1, chx2, chy1, chy2, chz1, chz2, chw1, chw2]))
    #                                 if ch_sum < len(incorrect_gates):
    #                                     continue

    #                                 new_gates = [g.copy() for g in initial_gates]
    #                                 new_gates[x1][-1], new_gates[x2][-1] = new_gates[x2][-1], new_gates[x1][-1]
    #                                 new_gates[y1][-1], new_gates[y2][-1] = new_gates[y2][-1], new_gates[y1][-1]
    #                                 new_gates[z1][-1], new_gates[z2][-1] = new_gates[z2][-1], new_gates[z1][-1]
    #                                 new_gates[w1][-1], new_gates[w2][-1] = new_gates[w2][-1], new_gates[w1][-1]

    #                                 if check_gates_correct(new_gates):
    #                                     print(','.join(sorted([x1, x2, y1, y2, z1, z2, w1, w2])))
    #                                     finished = True
    #                                     break
