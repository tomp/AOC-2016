#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 12
#
import re

INPUTFILE = 'input.txt'

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
            y = int(y)
        instructions.append((ins, x, y))
    return instructions

def execute(program, init_reg=None):
    size = len(program)

    reg = create_registers(['a', 'b', 'c', 'd'], init_reg)
    instructions = parse_program(program)

    pc = 0
    while pc < size:
        ins, x, y = instructions[pc]
        # line = "{} {} {}".format(ins, x, y)
        # print("{:03d}: {:10s}  {}".format(pc, line,
        #     "  ".join(["{}:{:2d}".format(r, reg[r]) for r in registers])))
        if ins == 'cpy':
            reg[y] = reg[x]
        elif ins == 'cpy_int':
            reg[y] = x
        elif ins == 'inc':
            reg[x] += 1
        elif ins == 'dec':
            reg[x] -= 1
        elif ins == 'jnz' and reg[x] != 0:
            pc += y
            continue
        elif ins == 'jnz_int' and x != 0:
            pc += y
            continue
        pc += 1
    return reg

def interpret(program, init_reg=None):
    registers = ['a', 'b', 'c', 'd']
    size = len(program)
    reg = dict([(name, 0) for name in registers])
    if init_reg is not None:
            reg.update(init_reg)
    pc = 0
    while pc < size:
        line = program[pc]
        parts = line.split()
        if len(parts) == 3:
            ins, x, y = parts
        elif len(parts) == 2:
            ins, x = parts
        else:
            raise ValueError("Bad instruction: '{}'".format(line))

        # print("{:03d}: {:10s}  {}".format(pc, line,
        #     "  ".join(["{}:{:2d}".format(r, reg[r]) for r in registers])))

        if ins == 'cpy':
            try:
                reg[y] = reg[x]
            except KeyError:
                reg[y] = int(x)
            pc += 1
        elif ins == 'inc':
            reg[x] += 1
            pc += 1
        elif ins == 'dec':
            reg[x] -= 1
            pc += 1
        elif ins == 'jnz':
            try:
                val = reg[x]
            except KeyError:
                val = int(x)
            if val != 0:
                pc += int(y)
            else:
                pc += 1
    return reg


def example():
    program = [ 'cpy 41 a',
                'inc a',
                'inc a',
                'dec a',
                'jnz a 2',
                'dec a' ]
    reg = execute(program)
    for x in sorted(reg.keys()):
        print("{}: {}".format(x, reg[x]))
    print('- ' * 32)
# PART 1

def part1(program):
    reg = execute(program)
    for x in sorted(reg.keys()):
        print("{}: {}".format(x, reg[x]))
    print('- ' * 32)


# PART 2

def part2(program):
    reg = execute(program, {'c': 1})
    for x in sorted(reg.keys()):
        print("{}: {}".format(x, reg[x]))
    print('- ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    part2(lines)
