from collections import defaultdict

MOVES = '<^>vA'
MOVE_MAP = {'<': -1, '>': +1, '^': -1j, 'v': +1j,}
NUM_PAD_MAP = {
    0+0j: '7', 1+0j: '8', 2+0j: '9',
    0+1j: '4', 1+1j: '5', 2+1j: '6',
    0+2j: '1', 1+2j: '2', 2+2j: '3',
               1+3j: '0', 2+3j: 'A',
}
KEY_PAD_MAP = {
               1+0j: '^', 2+0j: 'A',
    0+1j: '<', 1+1j: 'v', 2+1j: '>',
}
NUM_PAD_INV_MAP = {v: k for k, v in NUM_PAD_MAP.items()}
KEY_PAD_INV_MAP = {v: k for k, v in KEY_PAD_MAP.items()}


# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [line.strip() for line in f.readlines()]

def move_on_keypad(current, move):
    pos = KEY_PAD_INV_MAP[current]
    new_pos = pos + MOVE_MAP[move]
    return KEY_PAD_MAP.get(new_pos, False)

def move_on_numpad(current, move):
    pos = NUM_PAD_INV_MAP[current]
    new_pos = pos + MOVE_MAP[move]
    return NUM_PAD_MAP.get(new_pos, False)

def check_code(code, final):
    return final.startswith(code)

def string_assign(string, i, elem):
    return ''.join([string[:i], elem, string[i+1:]])

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

def heuristic(state):
    moves, _hash = state
    code, positions = _hash

    #return len(code)*(2**25) - len(moves)
    #return -(len(code)*25 - positions.count('A'))
    bigger_is_better = len(code) + len(moves)
    return -bigger_is_better


def walk_graph(final_code, robots=3):
    # State will be
    # Moves, (code, positions)
    # The hash here will be
    # code, positions
    paths = [('', ('', 'A'*robots))]
    history = dict()
    shortest_found = float("inf")

    while len(paths):
        current_state = paths.pop()
        moves, _hash = current_state
        code, positions = _hash
        print(f"*{code}* | {positions} | {len(paths)}")
        length = len(moves)

        if not check_code(code, final_code):
            continue

        if _hash in history and history[_hash] <= length:
            continue
        history[_hash] = length

        if code == final_code:
            shortest_found = min(length, shortest_found)

        if length >= shortest_found:
            continue

        for m in MOVES:
            new_moves = ''.join([moves,m])
            new_code = code
            new_positions = positions

            # This is on the human keypad
            if m=='A':
                for i, _m in enumerate(positions):
                    is_final = (i+1==len(positions))
                    is_second_final = (i+2==len(positions))

                    if is_final:
                        new_code = ''.join([code, _m])
                        break
                    elif _m != 'A':
                        which_func = move_on_numpad if is_second_final else move_on_keypad
                        next_pos = which_func(positions[i+1], _m)
                        if next_pos is False:
                            new_positions = ''
                        else:
                            new_positions = string_assign(new_positions, i+1, next_pos)
                        break
            else:
                next_pos = move_on_keypad(positions[0], m)
                if next_pos is False:
                    new_positions = ''
                else:
                    new_positions = string_assign(new_positions, 0, next_pos)

            if not new_positions:
                continue
            new_state = (new_moves, (new_code, new_positions))
            #paths.append(new_state)
            binary_insert(paths, new_state, heuristic)

    return history[(final_code, 'A'*robots)]


def complexity(shortest_length, code):
    return shortest_length*int(code[:-1])

# Main #
if __name__ == "__main__":
    data = load_data('data/day_21.dat')

    checksum_1 = sum((complexity(walk_graph(d, 3), d) for d in data))
    print(f"Part 1: {checksum_1}")

    #checksum_2 = sum((complexity(walk_graph(d, 26), d) for d in data))
    #print(f"Part 1: {checksum_2}")