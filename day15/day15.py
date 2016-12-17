#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 15
#
from collections import namedtuple

Disc = namedtuple('Disc', ['total', 'current'])

INPUT = [
    Disc(13, 1),
    Disc(19, 10),
    Disc(3,2),
    Disc(7, 1),
    Disc(5, 3),
    Disc(17, 5),
]

def discs_aligned(discs):
    """Find the time at which a ball could be dropped and find
    each disc at position 0 when the ball reached that disk,
    given the specified disc positions at time 0.
    """
    pos = [(disc.current, disc.total) for disc in discs]
    step = 0
    print("Slots:  {}".format(" ".join([str(p[1]) for p in pos])))
    print("{:5d}:  {}".format(step, " ".join([str((p[0]+idx+1)%p[1]) for idx, p in
        enumerate(pos)])))
    while any([(p[0]+idx+1)%p[1] > 0 for idx, p in enumerate(pos)]):
        pos = [((p[0]+1)%p[1], p[1]) for p in pos]
        step += 1
        # print("{:5d}:  {}".format(step, " ".join([str((p[0]+idx+1)%p[1]) for idx, p in
        #     enumerate(pos)])))
    return step

# Example

def example():
    discs = [
        Disc(5, 4),
        Disc(2, 1)
    ]

    t = discs_aligned(discs)
    print("t = {}".format(t))
    print('= ' * 32)

# PART 1

def part1(discs):
    t = discs_aligned(discs)
    print("t = {}".format(t))
    print('= ' * 32)


# PART 2

def part2(discs):
    t = discs_aligned(discs)
    print("t = {}".format(t))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    part1(INPUT)

    INPUT.append(Disc(11, 0))
    part2(INPUT)
