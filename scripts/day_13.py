P2_FACTOR = 10000000000000

# Helper functions #
def parse_group(group):
    a, b, c = group.split('\n')
    a = a.strip('Button A:')
    b = b.strip('Button B:')
    c = c.strip('Prize :')

    def line_helper(line):
        x, y = line.split(', ')
        x = x.strip('X+').strip('X=')
        y = y.strip('Y+').strip('Y=')
        return int(x), int(y)

    return [line_helper(l) for l in [a,b,c]]

def load_data(fname):
    with open(fname, 'r') as f:
        return [parse_group(g) for g in f.read().split('\n\n')]

def is_num_int(num):
    return num == int(num)

def solve_game(game, part_2=False):
    # N * a_dx + M * b_dx = x_goal
    # N * a_dy + M * b_dy = y_goal

    [a_dx, a_dy], [b_dx, b_dy], [x_goal, y_goal] = game
    if part_2:
        x_goal += P2_FACTOR
        y_goal += P2_FACTOR

    N = (x_goal * b_dy - y_goal * b_dx) / (a_dx * b_dy - a_dy * b_dx)
    M = (a_dx * y_goal - a_dy * x_goal) / (a_dx * b_dy - a_dy * b_dx)

    if is_num_int(N) and is_num_int(M):
        return int(N), int(M)
    return -1, -1


# Main #
if __name__ == "__main__":
    data = load_data('data/day_13.dat')

    checksum_1 = 0
    for game in data:
        n, m = solve_game(game)
        if n > 0 and m > 0:
            checksum_1 += 3*n + m
    print(f"Part 1: {checksum_1}")

    checksum_2 = 0
    for game in data:
        n, m = solve_game(game, part_2=True)
        if n > 0 and m > 0:
            checksum_2 += 3*n + m
    print(f"Part 2: {checksum_2}")