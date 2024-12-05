
import re

def load_data(fname):
    with open(fname, 'r') as f:
        return f.read().strip()


if __name__ == "__main__":
    data = load_data('data/day_03.dat')

    matches = re.findall("mul\((\d*),(\d*)\)", data)
    checksum = sum((int(a)*int(b) for a, b in matches))

    print(f"Part 1: {checksum}")

    data = f"do(){data}don't()"
    datas = [d for d in re.split("do\(\)", data) if d]
    datas = [re.split("don't\(\)", d)[0] for d in datas if d]

    checksum = 0
    for d in datas:
        matches = re.findall("mul\((\d*),(\d*)\)", d)
        checksum += sum((int(a)*int(b) for a, b in matches))
    print(f"Part 2: {checksum}")