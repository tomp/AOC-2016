#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 19
#
import math

INPUT = 3014603

def reduce_circle_calc(n):
    k = int(math.log(n, 2))
    return 2*(n - int(math.pow(2, k))) + 1

def reduce_circle_calc2(n):
    k = math.floor(math.log(n-1, 3))
    m = math.pow(3, k)
    d = n - m
    if d <= m:
        return int(d)
    else:
        return int(m + 2*(d - m))

def reduce_circle(size):
    """Redistribute gifts among the members of a circle of the given
    size, according to the puzzle descriptionn.

    The number of the elf with all the presents is returned
    """
    # print("{} elves in the circle".format(size))
    elves = [1] * size # array with state (1: has presents, 0: no presents)
                       # of each elf
    recv = 0 # index for the elf receiving presents
    give = 1 # index for the elf losing presents
    while give != recv:
        # print("Elf {} takes Elf {}'s presents".format(recv+1, give+1))
        elves[give] = 0
        recv = (give + 1) % size
        while elves[recv] == 0:
            recv = (recv + 1) % size
        give = (recv + 1) % size
        while elves[give] == 0:
            give = (give + 1) % size
    return recv + 1

def reduce_circle2(size):
    """Redistribute gifts among the members of a circle of the given
    size, according to the part-2 puzzle descriptionn.
    """
    elves = [idx+1 for idx in range(size)] # list of remaining elves
    recv = 0
    # print("{} elves in the circle".format(size))
    remaining = len(elves)
    assert(remaining == size)
    while remaining > 1:
        # print("Elf {}: circle: {}".format(elves[recv], " ".join([str(x)
        #     for x in elves])))
        elf1 = elves[recv]
        delt = remaining // 2
        give = (recv + delt) % remaining
        elf2 = elves[give]
        # print("[{}] Elf {} takes Elf {}'s presents".format(remaining, elf1, elf2))
        elves.pop(give)
        remaining -= 1
        if give > recv:
            recv = (recv + 1) % remaining
        else:
            recv = recv % remaining
    return elves[0]

# Example

def example():
    input = 5
    expected = 3
    elf = reduce_circle(input)
    print("Elf {} gets all the loot".format(elf))
    assert(elf == expected)
    print('- ' * 32)
    expected = 2
    elf = reduce_circle2(input)
    print("Elf {} gets all the loot".format(elf))
    print('= ' * 32)

def explore():
    for n in range(3,64):
        elf = reduce_circle2(n)
        print("N={}  ELf {} wins".format(n, elf))
    print('= ' * 32)

# PART 1

def part1(input):
    # elf = reduce_circle(input)
    elf = reduce_circle_calc(input)
    print("Elf {} gets all the loot".format(elf))
    print('= ' * 32)


# PART 2

def part2(input):
    # elf = reduce_circle2(input)
    elf = reduce_circle_calc2(input)
    print("Elf {} gets all the loot".format(elf))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    # explore()
    part1(INPUT)
    part2(INPUT)
