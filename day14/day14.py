#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day N
#
from hashlib import md5
import re

INPUT = 'jlmsuwbz'

triplet_re = re.compile(r"(.)\1\1")

def key_gen(idx, salt, iter=0):
    input = "{}{}".format(salt,idx)
    key = md5(input.encode()).hexdigest()
    for i in range(iter):
        key = md5(key.encode()).hexdigest()
    return key

def key_stream(salt, iter=0):
    """Return a stream of keys, generated using the given salt."""
    buffer = [(i, key_gen(i, salt, iter)) for i in range(1001)]
    idx = 1001
    while True:
        i, key = buffer.pop(0)
        buffer.append((idx, key_gen(idx, salt, iter)))
        idx += 1

        m = triplet_re.search(key)
        if m is None:
            continue
        ch5 = m.group(1) * 5
        if any([ch5 in item[1] for item in buffer]):
            yield i, key 

# Example

def example(salt):
    for n, item in enumerate(key_stream(salt)):
        idx, key = item
        print("[{:2d}] idx: {}  key: {}".format(n+1, idx,
            key_gen(idx, salt)))
        if n == 64:
            break
    print('= ' * 32)

# PART 1

def part1(salt):
    for n, item in enumerate(key_stream(salt)):
        idx, key = item
        print("[{:2d}] idx: {}  key: {}".format(n+1, idx,
            key_gen(idx, salt)))
        if n == 64:
            break
    print('= ' * 32)


# PART 2

def part2(salt):
    for n, item in enumerate(key_stream(salt, 2016)):
        idx, key = item
        print("[{:2d}] idx: {}  key: {}".format(n+1, idx,
            key_gen(idx, salt)))
        if n == 64:
            break
    print('= ' * 32)

if __name__ == '__main__':
    example('abc')
    part1(INPUT)
    part2(INPUT)
