

def load_data_int(fname):
    with open(fname, 'r') as f:
        data = f.read().splitlines()
    a = [int(x.split('   ')[0]) for x in data]
    b = [int(x.split('   ')[1]) for x in data]
    return a, b

if __name__ == "__main__":
    a, b = load_data_int('data/day_01.dat')

    a = sorted(a)
    b = sorted(b)

    ans = sum([
        max(aa, bb) - min(aa, bb) for aa, bb in zip(a, b)
    ])

    print(ans)

    ans_b = 0

    for aa in a:
        count = b.count(aa)
        ans_b += count*aa

    print(ans_b)