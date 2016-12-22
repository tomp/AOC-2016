#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 19
#

INPUT = 3014603

def reduce_circle(size):
    """Redistribute gifts among the members of a circle of the given
    size, according to the puzzle descriptionn.
    """
    active = [1] * size
    last = 0
    next = 1
    print("[reduce] {} elves in the circle".format(size))
    while next != last:
        # print("Elf {} takes Elf {}'s presents".format(last+1, next+1))
        active[next] = 0
        last = (next + 1) % size
        while active[last] == 0:
            last = (last + 1) % size
        next = (last + 1) % size
        while active[next] == 0:
            next = (next + 1) % size
    return last

def reduce_circle2(size):
    """Redistribute gifts among the members of a circle of the given
    size, according to the puzzle descriptionn.
    """
    active = [idx+1 for idx in range(size)]
    last = 0
    print("[reduce2] {} elves in the circle".format(size))
    remaining = len(active)
    assert(remaining == size)
    while remaining > 1:
        # print("Elf {}: circle: {}".format(active[last], " ".join([str(x)
        #     for x in active])))
        elf1 = active[last]
        delt = remaining // 2
        next = (last + delt) % remaining
        elf2 = active[next]
        print("[{}] Elf {} takes Elf {}'s presents".format(remaining, elf1, elf2))
        active.pop(next)
        remaining -= 1
        if next > last:
            last = (last + 1) % remaining
        else:
            last = last % remaining
    return active[0]

# Example

def example():
    input = 5
    elf = reduce_circle(input)
    print("Elf {} gets all the loot".format(elf+1))
    print('- ' * 32)
    elf = reduce_circle2(input)
    print("Elf {} gets all the loot".format(elf))
    print('= ' * 32)

# PART 1

def part1(input):
    elf = reduce_circle(input)
    print("Elf {} gets all the loot".format(elf+1))
    print('= ' * 32)


# PART 2

def part2(input):
    elf = reduce_circle2(input)
    print("Elf {} gets all the loot".format(elf))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    part1(INPUT)
    part2(INPUT)
