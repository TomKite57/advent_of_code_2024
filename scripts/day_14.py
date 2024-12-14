from collections import defaultdict

MAP_X, MAP_Y = 101, 103

# Helper functions #
def parse_line(line):
    p, v = line.split(' ')
    p = p.strip('p=')
    v = v.strip('v=')
    px, py = [int(x) for x in p.split(',')]
    vx, vy = [int(x) for x in v.split(',')]
    return [(px, py), (vx, vy)]

def load_data(fname):
    with open(fname, 'r') as f:
        return [parse_line(g) for g in f.readlines()]

def evolve_pos(pp, vv, steps):
    px, py = pp
    vx, vy = vv

    nx = (px + steps*vx)%MAP_X
    ny = (py + steps*vy)%MAP_Y

    return nx, ny

def get_quadrant(all_pp):
    nums = [0 for _ in range(4)]
    for px, py in all_pp:
        if px == MAP_X//2 or py == MAP_Y//2:
            continue
        ind = int(f"{int(px>MAP_X//2)}{int(py>MAP_Y//2)}", 2)
        nums[ind] += 1
    return nums

def quadrant_checksum(quad):
    prod = 1
    for n in quad:
        prod *= n
    return prod

def show_space(all_pp):
    pp_set = set(all_pp)
    for x in range(MAP_X):
        for y in range(MAP_Y):
            if (x, y) not in pp_set:
                print('.', end='')
            else:
                print('X', end='')
        print()

def explore_current_island(pp_set, loc):
    seen = set()
    seen.add(loc)
    path = [loc]
    while len(path):
        l = path.pop()
        x, y = loc
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (x+dx, y+dy) in pp_set and (x+dx, y+dy) not in seen:
                    seen.add((x+dx, y+dy))
                    path.append((x+dx, y+dy))
    return seen

def get_biggest_island(all_pp):
    seen = set()
    islands = []
    pp_set = set(all_pp)
    for pp in pp_set:
        if pp in seen:
            continue
        island = explore_current_island(pp_set, pp)
        seen |= island
        islands.append(island)

    return max([len(i) for i in islands])

# Main #
if __name__ == "__main__":
    data = load_data('data/day_14.dat')

    all_future_pos = [evolve_pos(pp, vv, 100) for [pp, vv] in data]
    checksum_1 = quadrant_checksum(get_quadrant(all_future_pos))
    print(f"Part 1: {checksum_1}")

    time = 0
    running_biggest = 0
    while True:
        pos = [evolve_pos(pp, vv, time) for [pp, vv] in data]
        biggest_island = get_biggest_island(pos)
        if biggest_island > running_biggest:
            running_biggest = biggest_island
            show_space(pos)
            print(f"Time: {time}")
            while True:
                print("Keep going? [y/n]")
                ans = input().lower()
                if ans == 'n':
                    done = True
                    break
                elif ans == 'y':
                    done = False
                    break
                else:
                    print("Did not understand answer.")
            if done:
                break
        #show_space(pos)
        time += 1




