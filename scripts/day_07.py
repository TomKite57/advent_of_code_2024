import itertools

# Helper functions #
def parse_line(line):
    result, factors = line.strip().split(": ")
    result = int(result)
    factors = [int(x) for x in factors.split(' ')]
    return result, factors

def load_data(fname):
    with open(fname, 'r') as f:
        return list(map(parse_line, f.readlines()))

def do_op(factors, operators):
    result = factors[0]
    for o, f in zip(operators, factors[1:]):
        if o == '+':
            result += f
        elif o == '*':
            result *= f
        elif o == '|':
            result = int(''.join([str(result), str(f)]))
        else:
            raise Exception(f"Did not understand operator {o}")
    return result

def valid_equation(result, factors, op_types):
    num_operators = len(factors)-1

    for ops in itertools.product(op_types, repeat=num_operators):
        test_result = do_op(factors, ops)
        if test_result == result:
            return True
    return False

# Main #
if __name__ == "__main__":
    data = load_data('data/day_07.dat')

    checksum_1 = sum((r for r, f in data if valid_equation(r, f, '+*')))
    print(f"Part 1: {checksum_1}")

    checksum_2 = sum((r for r, f in data if valid_equation(r, f, '+*|')))
    print(f"Part 1: {checksum_2}")
