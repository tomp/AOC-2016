#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 16
#

INPUT = '10111011111001111'
SIZE = 272
SIZE2 = 35651584

def expand(input, min_size=0):
    """Expand the input text to the given size using the "modified
    Dragon curve" described in the Day 16 instructions.
    The input string should consist entirely of '0' and '1' characters.
    """
    assert(min_size > 0)
    assert(input.count('0') + input.count('1') == len(input))
    result = input
    while len(result) < min_size:
        mirror = [('0' if ch == '1' else '1') for ch in reversed(result)]
        result = result + '0' + "".join(mirror)
    return result

def checksum(input):
    """Calculate the checksum of the input text, as described in the
    Day 16 instructions.
    """
    result = input
    while len(result) % 2 == 0:
        digits = []
        for i in range(0,len(result), 2):
            if result[i:i+2] == '00' or result[i:i+2] == '11':
                digits.append('1')
            else:
                digits.append('0')
        result = "".join(digits)
    return result

def fill_disk(init_state, size):
    """Expand the given init_state string to fill a disk of the given
    size.  The final string and its checksum are returned.
    """
    final_state = expand(init_state, size)[:size]
    cksum = checksum(final_state)
    return final_state, cksum

# Example

def example():
    CASES = [('1', '100'),
             ('0', '001'),
             ('11111', '11111000000'),
             ('111100001010', '1111000010100101011110000')]
    for input, expected in CASES:
        result = expand(input, len(input)+1)
        print("'{}' --> '{}'  (expected '{}')".format(input, result,
            expected))
        assert(result == expected)

    input = '110010110100'
    expected = '100'
    cksum = checksum(input)
    print("checksum('{}') --> '{}'  (expected '{}')".format(input,
        cksum, expected))
    assert(cksum == expected)
    print('- ' * 32)

    init_state = '10000'
    size = 20
    expected_cksum = '01100'
    final_state, cksum = fill_disk(init_state, size)
    print("initial: '{}'".format(init_state))
    print("final:   '{}'".format(final_state))
    print("checksum = '{}'  (expected '{}')".format(cksum,
        expected_cksum))
    assert(len(final_state) == size)
    assert(cksum == expected_cksum)
    print('= ' * 32)

# PART 1

def part1(input, size):
    final_state, cksum = fill_disk(input, size)
    print("initial: '{}'".format(input))
    print("final:   '{}'".format(final_state))
    print("checksum = '{}'".format(cksum))
    print('= ' * 32)


# PART 2

def part2(input, size):
    final_state, cksum = fill_disk(input, size)
    print("initial: '{}'".format(input))
    # print("final:   '{}'".format(final_state))
    print("checksum = '{}'".format(cksum))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    part1(INPUT, SIZE)
    part2(INPUT, SIZE2)
