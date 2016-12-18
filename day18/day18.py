#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day N
#

INPUT = '.^^^^^.^^.^^^.^...^..^^.^.^..^^^^^^^^^^..^...^^.^..^^^^..^^^^...^.^.^^^^^^^^....^..^^^^^^.^^^.^^^.^^'

TRAP = '^'
TILE = '.'

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

def next_row(row):
    n = len(row)
    next = ["."] * n
    for i, t in enumerate(row):
        if i == 0:
            if row[i+1] == TRAP:
                next[i] = TRAP
        elif i == n - 1:
            if row[n-2] == TRAP:
                next[n-1] = TRAP
        elif row[i-1] == TRAP and row[i+1] != TRAP:
            next[i] = TRAP
        elif row[i-1] != TRAP and row[i+1] == TRAP:
            next[i] = TRAP
    return "".join(next)

# Example

def example():
    row1 = '..^^.'
    expected2 = '.^^^^'
    expected3 = '^^..^'
    row2 = next_row(row1)
    row3 = next_row(row2)
    print("row 1: {}".format(row1))
    print("row 2: {}".format(row2))
    assert(row2 == expected2)
    print("row 3: {}".format(row3))
    assert(row3 == expected3)


    row1 = ".^^.^.^^^^"
    expected = """
.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^
""".strip()
    rows = [row1]
    for i in range(9):
        rows.append(next_row(rows[i]))
    rows_str = "\n".join(rows)
    print(rows_str)
    assert(rows_str == expected)

    count = rows_str.count(TILE)
    print("{} safe tiles".format(count))
    print('= ' * 32)

# PART 1

def part1(row1, nrows):
    safe = row1.count(TILE)
    row = row1
    for i in range(nrows-1):
        row = next_row(row)
        safe += row.count(TILE)

    print("{} safe tiles".format(safe))
    print('= ' * 32)


# PART 2

def part2(row1, nrows):
    rows = [row1]
    for i in range(nrows-1):
        rows.append(next_row(rows[i]))
    rows_str = "\n".join(rows)
    # print(rows_str)

    count = rows_str.count(TILE)
    print("{} safe tiles".format(count))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    part1(INPUT, 40)
    part2(INPUT, 400000)
