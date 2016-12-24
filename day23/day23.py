#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 23
#
import re
import math

INPUTFILE = 'input.txt'
INPUT = 7
INPUT2 = 12

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

def create_registers(names, init_reg=None):
    registers = ['a', 'b', 'c', 'd']
    reg = dict([(name, 0) for name in registers])
    if init_reg is not None:
        reg.update(init_reg)
    return reg

def parse_program(program):
    instructions = []
    for line in program:
        parts = line.split()
        if len(parts) == 3:
            ins, x, y = parts
        elif len(parts) == 2:
            ins, x = parts
            y = ""
        else:
            raise ValueError("Bad instruction: '{}'".format(line))
        try:
            x = int(x)
            ins += "_int"
        except ValueError:
            pass
        if ins.startswith('jnz'):
            try:
                y = int(y)
            except ValueError:
                pass
        instructions.append((ins, x, y))
    return instructions

def execute(program, init_reg=None):
    size = len(program)

    reg = create_registers(['a', 'b', 'c', 'd'], init_reg)
    instructions = parse_program(program)

    pc = 0
    while pc < size:
        ins, x, y = instructions[pc]
        line = "{} {} {}".format(ins, x, y)
        if pc == 16:
            print("{:03d}: {:10s}  {}".format(pc, line,
                "  ".join(["{}:{:2d}".format(r, reg[r]) for r in
                    sorted(reg.keys())])))
        try:
            if ins == 'tgl':
                addr = pc + reg[x]
                toggle(instructions, addr)
            elif ins == 'cpy':
                reg[y] = reg[x]
            elif ins == 'cpy_int':
                reg[y] = x
            elif ins == 'mul_int':
                reg['a'] = reg[x] * reg[y]
            elif ins == 'inc':
                if y == "":
                    reg[x] += 1
            elif ins == 'dec':
                if y == "":
                    reg[x] -= 1
            elif ins == 'jnz' and reg[x] != 0:
                try:
                    pc += y
                except TypeError:
                    pc += reg[y]
                continue
            elif ins == 'jnz_int' and x != 0:
                try:
                    pc += y
                except TypeError:
                    pc += reg[y]
                continue
        except KeyError:
            pass
        # print("{:03d}: {:10s}  {}".format(pc, line,
        #     "  ".join(["{}:{:2d}".format(r, reg[r]) for r in
        #         sorted(reg.keys())])))
        pc += 1
    return reg

def toggle(instructions, addr):
    if addr < 0 or addr > len(instructions)-1:
        print("Toggle: '[{}]".format(addr))
        return
    ins, x, y = instructions[addr]
    ins_orig = ins
    if y == "":
        if ins == 'inc':
            ins = 'dec'
        else:
            ins = 'inc'
    else:
        if ins.startswith('jnz'):
            ins = 'cpy' + ins[3:]
        else:
            ins = 'jnz' + ins[3:]
    instructions[addr] = (ins, x, y)
    print("Toggle: '[{}] {} {} {}' --> '{} {} {}'".format(addr,
        ins_orig, x, y, ins, x, y))

def example():
    program = [ 'cpy 2 a',
                'tgl a',
                'tgl a',
                'tgl a',
                'cpy 1 a',
                'dec a',
                'dec a' ]
    expected = 3
    reg = execute(program)
    for x in sorted(reg.keys()):
        print("{}: {}".format(x, reg[x]))
        assert(reg['a'] == expected)
    print('- ' * 32)

    # a -> b * d
    program = [
        'cpy 0 a',
        'cpy b c',
        'inc a',
        'dec c',
        'jnz c -2',
        'dec d',
        'jnz d -5']
    reg = execute(program, {'b': 5, 'd':12})
    for x in sorted(reg.keys()):
        print("{}: {}".format(x, reg[x]))
    print('- ' * 32)
# PART 1

def part1(value, program):
    reg = execute(program, {'a': value})
    for x in sorted(reg.keys()):
        print("{}: {}".format(x, reg[x]))

    result = reg['a']
    print("Result is {}".format(result))
    expected = math.factorial(value) + (81 * 94)
    assert(result == expected)
    print('- ' * 32)


# PART 2

def part2(value):
    result = math.factorial(value) + (81 * 94)
    print("Result is {}".format(result))
    print('- ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(INPUT, lines)
    part2(INPUT2)
