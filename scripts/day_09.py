# This is far from my best code... I am on an early morning flight and very sleepy :')

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        return [int(x) for x in f.read().strip()]

def print_disk(sizes, ids):
    for i, (_id, s) in enumerate(zip(ids, sizes)):
        if s==0:
            continue
        if i%2==1:
            print('.'*s, end='')
        else:
            print(f'{_id}'*s, end='')
    print()


def part_1(data):
    disk = [0]*sum(data)
    cum_i = 0
    for i, v in enumerate(data):
        if i%2 == 0:
            disk[cum_i:cum_i + v] = [i//2]*v
        else:
            disk[cum_i:cum_i + v] = [-1]*v
        cum_i += v

    checksum = 0
    pi, pj = 0, len(disk)-1
    while pi <= pj:
        while disk[pj]==-1 and pi <= pj:
            pj -= 1
        if pi > pj:
            break

        vi, vj = disk[pi], disk[pj]
        if vi == -1:
            checksum += vj*pi
            pi += 1
            pj -=1
        else:
            checksum += vi*pi
            pi += 1
    return checksum

def part_2(data):
    ids = [i//2 if i%2==0 else 0 for i, _ in enumerate(data)]

    new_data = [x for x in data]
    new_ids = [i for i in ids]

    is_data = lambda ind: ind%2 == 0
    is_space = lambda ind: not is_data(ind)

    j = len(new_data)-1
    #print_disk(data, ids)
    while j>=0:
        if is_space(j):
            j -= 1
            continue

        size = new_data[j]
        _id = new_ids[j]
        for i in range(j):
            if is_data(i):
                continue
            space = new_data[i]
            if space >= size:
                new_data[i] = 0
                new_data.insert(i+1, size)
                new_data.insert(i+2, space-size)
                new_ids.insert(i+1, _id)
                new_ids.insert(i+2, 0)

                j += 2
                new_data[j] = 0
                new_data[j-1] += size
                #print_disk(new_data, new_ids)


                break

        j -= 1

    #print_disk(new_data, new_ids)
    checksum = 0
    running_i = 0
    for i, (_id, s) in enumerate(zip(new_ids, new_data)):
        for j in range(s):
            checksum += _id*running_i
            running_i += 1
    return checksum




# Main #
if __name__ == "__main__":
    data = load_data('data/day_09.dat')

    checksum_1 = part_1(data)
    print(f"Part 1: {checksum_1}")

    checksum_2 = part_2(data)
    print(f"Part 2: {checksum_2}")
