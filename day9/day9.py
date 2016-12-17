#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day N
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

marker_re = re.compile(r"\((\d+)x(\d+)\)")

def expand1(text):
    """Expand the input text according to the '(extent x repeat)'
    scheme.  The output is the expanded text.
    """
    result = []
    pos = 0
    m = marker_re.search(text[pos:])
    # print("Input text size: {}".format(len(text)))
    # print("pos {}".format(pos), m)
    while m:
        start, size = m.start(), len(m.group())
        result.append(text[pos:start])

        extent, repeat = int(m.group(1)), int(m.group(2))
        pos += start + size
        result.append(text[pos:pos+extent] * repeat)

        pos += extent
        m = marker_re.search(text[pos:])
        # print("pos {}  match: {}".format(pos, m))
    result.append(text[pos:])
    return "".join(result)

def expand2(text):
    """Expand the input text according to version 2 of the
    '(extent x repeat)' scheme.  The output is the length of
    the expanded text.
    """
    result = 0
    remaining_text = str(text)
    # print("[2] Input text size: {}".format(len(text)))

    m = marker_re.search(remaining_text)
    while m:
        start, size = m.start(), len(m.group())
        result += start

        extent, repeat = int(m.group(1)), int(m.group(2))
        pos = start + size
        expanded_section = remaining_text[pos:pos+extent] * repeat

        pos += extent
        remaining_text = expanded_section + remaining_text[pos:]
        m = marker_re.search(remaining_text)
        # print("[2] result {}  pos {}  remaining {}  match: {}".format(
        #     result, pos, len(remaining_text), m))
    result += len(remaining_text)
    # print("[2] FINAL RESULT {}".format(result))
    return result

def expand3(text):
    """Expand the input text according to version 2 of the
    '(extent x repeat)' scheme.  The output is the length of
    the expanded text.

    This is a recursive version of expand2().
    """
    result = 0
    remaining_text = str(text)
    # print("[3] Input text size: {}".format(len(text)))

    m = marker_re.search(remaining_text)
    while m:
        start, size = m.start(), len(m.group())
        result += start

        extent, repeat = int(m.group(1)), int(m.group(2))
        pos = start + size
        assert(pos + extent <= len(remaining_text))
        result += expand3(remaining_text[pos:pos+extent]) * repeat

        pos += extent
        remaining_text = remaining_text[pos:]
        m = marker_re.search(remaining_text)
        # print("[3] result {}  pos {}  remaining {}  match: {}".format(
        #     result, pos, len(remaining_text), m))
    result += len(remaining_text)
    # print("[3] FINAL RESULT {}".format(result))
    return result


# Example

def example1():
    cases = [
        ('ADVENT', 'ADVENT'),
        ('A(1x5)BC', 'ABBBBBC'),
        ('(3x3)XYZ', 'XYZXYZXYZ'),
        ('(3x3)XYZ(2x2)ABC', 'XYZXYZXYZABABC'),
        ('(6x1)(1x3)A', '(1x3)A'),
        ('X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY')]

    for text, expected in cases:
        print("'{}' --> '{}'".format(text, expand1(text)))
        assert(expand1(text) == expected)

def example2():
    cases = [
        ('ADVENT', len('ADVENT')),
        ('A(1x5)BC', len('ABBBBBC')),
        ('(3x3)XYZ', len('XYZXYZXYZ')),
        ('(3x3)XYZ(2x2)ABC', len('XYZXYZXYZABABC')),
        ('(6x1)(1x3)A', len('AAA')),
        ('X(8x2)(3x3)ABCY', len('XABCABCABCABCABCABCY')),
        ('(27x12)(20x12)(13x14)(7x10)(1x12)A', 241920),
        ('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445)]

    for text, expected in cases:
        expanded = expand2(text)
        print("'{}' --> {} characters".format(text, expanded))
        assert(expanded == expected)

def example3():
    cases = [
        ('ADVENT', len('ADVENT')),
        ('A(1x5)BC', len('ABBBBBC')),
        ('(3x3)XYZ', len('XYZXYZXYZ')),
        ('(3x3)XYZ(2x2)ABC', len('XYZXYZXYZABABC')),
        ('(6x1)(1x3)A', len('AAA')),
        ('X(8x2)(3x3)ABCY', len('XABCABCABCABCABCABCY')),
        ('(27x12)(20x12)(13x14)(7x10)(1x12)A', 241920),
        ('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445)]

    for text, expected in cases:
        expanded = expand3(text)
        print("'{}' --> {} characters".format(text, expanded))
        assert(expanded == expected)

    

# PART 1

def part1(input):
    print("Input text length: {},  output length: {}".format(len(input),
        len(expand1(input))))
    print('- ' * 32)


# PART 2

def part2(input):
    print("Input text length: {},  output length: {}".format(len(input),
        expand3(input)))
    print('- ' * 32)

if __name__ == '__main__':
    lines = load_input(INPUTFILE)
    input = lines[0]

    example1()
    part1(input)

    example2()
    example3()
    part2(input)
