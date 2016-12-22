#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 21
#
import re

INPUTFILE = 'input.txt'

INPUT2 = 'fbgdceah'

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

SWAP_POS_RE = re.compile(r"swap position (\d) with position (\d)$")
SWAP_LETTER_RE = re.compile(r"swap letter ([a-z]) with letter ([a-z])$")
REVERSE_POS_RE = re.compile(r"reverse positions (\d) through (\d)$")
ROTATE_LETTER_RE = re.compile(r"rotate based on position of letter ([a-z])$")
MOVE_POS_RE = re.compile(r"move position (\d) to position (\d)$")
ROTATE_LEFT_RE = re.compile(r"rotate left (\d) steps?$")
ROTATE_RIGHT_RE = re.compile(r"rotate right (\d) steps?$")

def swap_pos(text, pos1, pos2, reverse=False):
    chars = [ch for ch in text]
    pos1 = int(pos1)
    pos2 = int(pos2)
    ch1, ch2 = chars[pos1], chars[pos2]
    chars[pos2] = ch1
    chars[pos1] = ch2
    return "".join(chars)

def swap_letter(text, let1, let2, reverse=False):
    pos1 = text.index(let1)
    pos2 = text.index(let2)
    return swap_pos(text, pos1, pos2)

def reverse_pos(text, start, stop, reverse=False):
    chars = [ch for ch in text]
    start = int(start)
    stop = int(stop)
    snip = reversed(chars[start:stop+1])
    chars[start:stop+1] = snip
    return "".join(chars)

def rotate_left(text, n, reverse=False):
    if reverse:
        return rotate_right(text, n)
    chars = [ch for ch in text]
    n = int(n) % len(chars)
    chars = chars[n:] + chars[:n]
    return "".join(chars)

def rotate_right(text, n, reverse=False):
    if reverse:
        return rotate_left(text, n)
    chars = [ch for ch in text]
    n = int(n) % len(chars)
    chars = chars[-n:] + chars[:-n] 
    return "".join(chars)
    
def move_pos(text, pos1, pos2, reverse=False):
    if reverse:
        return move_pos(text, pos2, pos1)
    chars = [ch for ch in text]
    pos1 = int(pos1)
    pos2 = int(pos2)
    ch1 = chars.pop(pos1)
    chars.insert(pos2, ch1)
    return "".join(chars)

def rotate_letter(text, let1, reverse=False):
    pos1 = text.index(let1)
    if reverse:
        if pos1 == 0:
            n = 1
        elif pos1 % 2 == 1:
            n = (pos1 + 1) // 2
        else:
            n = (pos1 // 2) + 5
        return rotate_left(text, n)
    if pos1 >= 4:
        n = 2 + pos1
    else:
        n = 1 + pos1
    n = n % len(text)
    # print('## pos={} --> rotate_right({})'.format(pos1, n))
    return rotate_right(text, n)
    
OPS = [
    (SWAP_POS_RE, swap_pos),
    (SWAP_LETTER_RE, swap_letter),
    (REVERSE_POS_RE, reverse_pos),
    (MOVE_POS_RE, move_pos),
    (ROTATE_LEFT_RE, rotate_left),
    (ROTATE_RIGHT_RE, rotate_right),
    (ROTATE_LETTER_RE, rotate_letter),
]

def execute_command(text, cmd, reverse=False):
    """Parse the command string and execute the specified operation
    on the given text.
    The resulting text is returned.
    """
    for pattern, action in OPS:
        m = pattern.match(cmd)
        if m:
            result = action(text, *m.groups(), reverse=reverse)
            return result
    raise ValueError("Command '{}' not recognized".format(cmd))

# Example

def example():
    # Test that each operation basically works correctly
    input = 'abcde'
    print("'{}'".format(input))
    text = swap_pos(input, 4, 0)
    print("  --> '{}'".format(text))
    assert(text == 'ebcda')

    text = swap_letter(text, 'd', 'b')
    print("  --> '{}'".format(text))
    assert(text == 'edcba')

    text = reverse_pos(text, 0, 4)
    print("  --> '{}'".format(text))
    assert(text == 'abcde')

    text = rotate_left(text, 1)
    print("  --> '{}'".format(text))
    assert(text == 'bcdea')

    text = move_pos(text, 1, 4)
    print("  --> '{}'".format(text))
    assert(text == 'bdeac')

    text = move_pos(text, 3, 0)
    print("  --> '{}'".format(text))
    assert(text == 'abdec')

    text = rotate_letter(text, 'b')
    print("  --> '{}'".format(text))
    assert(text == 'ecabd')

    text = rotate_letter(text, 'd')
    print("  --> '{}'".format(text))
    assert(text == 'decab')

    text = rotate_right(text, 3)
    print("  --> '{}'".format(text))
    assert(text == 'cabde')

    print('- ' * 32)

    # Test that the commands are parsed executed correctly
    lines = [
        ('swap position 4 with position 0', 'ebcda'),
        ('swap letter d with letter b', 'edcba'),
        ('reverse positions 0 through 4', 'abcde'),
        ('rotate left 1 step', 'bcdea'),
        ('move position 1 to position 4','bdeac'), 
        ('move position 3 to position 0', 'abdec'),
        ('rotate based on position of letter b', 'ecabd'),
        ('rotate based on position of letter d', 'decab'),
    ]
    text = input
    rev_lines = []
    print("'{}'".format(input))
    for line, expected in lines:
        rev_lines.append((line, text))
        text = execute_command(text, line)
        print("  --> '{}'".format(text))
        assert(text == expected)
    print("'{}' --> '{}'".format(input, text))
    print('- ' * 32)

    # Test that the reversed operations basically work correctly.
    input2 = text
    for line, expected in reversed(rev_lines):
        text = execute_command(text, line, reverse=True)
        print("reverse: {:36s} --> '{}'".format(line, text))
        assert(text == expected)
    print("'{}' --> '{}'".format(input2, text))
    assert(text == input)
    print('= ' * 32)

# PART 1

def part1(lines):
    input = 'abcdefgh'
    print("'{}'".format(input))
    text = input
    for line in lines:
        text = execute_command(text, line)
        print("{:36s} --> '{}'".format(line, text))
    print("'{}' --> '{}'".format(input, text))
    print('- ' * 32)

    # Test that reversed operations are correct by trying to
    # recover the input string for this part.
    input2 = text
    for line in reversed(lines):
        text = execute_command(text, line, reverse=True)
        print("reverse: {:36s} --> '{}'".format(line, text))
    print("'{}' --> '{}'".format(input2, text))
    assert(text == input)
    print('= ' * 32)


# PART 2

def part2(lines, input2):
    text = input2
    for line in reversed(lines):
        text = execute_command(text, line, reverse=True)
        print("reverse: {:36s} --> '{}'".format(line, text))
    print("'{}' --> '{}'".format(input2, text))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    part2(lines, INPUT2)
