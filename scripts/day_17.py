from math import log2

# Helper functions #
def load_data(fname):
    with open(fname, 'r') as f:
        raw_lines = f.read()

    regs, ops = raw_lines.split('\n\n')
    regs = regs.split('\n')
    regs = [int(r.split(': ')[1]) for r in regs]
    ops = [int(x) for x in ops.split(': ')[1].split(',')]

    return regs, ops

class Computer:
    def __init__(self, regs, ops):
        self.A = regs[0]
        self.B = regs[1]
        self.C = regs[2]
        self.ops = ops
        self.pointer = 0
        self.func_dict = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }
        self.output = []

    def run(self):
        while self.pointer < len(ops):
            self.func_dict[self.ops[self.pointer]](self.ops[self.pointer+1])
            self.pointer += 2
        return self.output

    def get_combo(self, x):
        if 0<=x<=3:
            return x
        if x==4:
            return self.A
        if x==5:
            return self.B
        if x==6:
            return self.C
        raise Exception("Invalid combo code")

    def adv(self, x):
        self.A = int(self.A/2**self.get_combo(x))

    def bxl(self, x):
        self.B = self.B ^ x

    def bst(self, x):
        self.B = self.get_combo(x)%8

    def jnz(self, x):
        if self.A != 0:
            self.pointer = x-2

    def bxc(self, x):
        self.B = self.B ^ self.C

    def out(self, x):
        self.output.append(str(self.get_combo(x)%8))

    def bdv(self, x):
        self.B = int(self.A/2**self.get_combo(x))

    def cdv(self, x):
        self.C = int(self.A/2**self.get_combo(x))

def register_macro(regs, ops, a_reg):
    computer = Computer(regs, ops)
    computer.A = a_reg
    out = computer.run()
    return out

# Main #
if __name__ == "__main__":
    regs, ops = load_data('data/day_17.dat')

    computer = Computer(regs, ops)
    out = computer.run()
    print(f"Part 1: {','.join(out)}")

    n = 0
    while True:
        a_reg = 8**n
        out = register_macro(regs, ops, a_reg)
        if len(out) < len(ops):
            n += 1
        else:
            break

    while True:
        current_out = register_macro(regs, ops, a_reg)
        if [int(x) for x in current_out] == [int(x) for x in ops]:
            break

        for ind in range(len(ops)-1, -1, -1):
            if int(current_out[ind]) != int(ops[ind]):
                a_reg += 8**ind
                break

    print(f"Part 2: {a_reg}")