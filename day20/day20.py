#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day N
#
from collections import namedtuple

INPUTFILE = 'input.txt'

MAXINT = 4294967295

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

Range = namedtuple('Range', ['min', 'max'])

class RangeSet(object):
    def __init__(self, r):
        assert(r.min >= 0)
        assert(r.max >= r.min)
        self.intervals = [r]

    def __str__(self):
        lines = []
        for r in self.intervals:
            lines.append("{}-{}".format(r.min, r.max))
        return("\n".join(lines))

    def exclude(self,  x):
        result = []
        for r in self.intervals:
            if r.max < x.min or x.max < r.min:
                result.append(r)
                continue
            if r.max >= x.min:
                if r.min < x.min:
                    result.append(Range(r.min, x.min-1))
                if r.max > x.max:
                    result.append(Range(x.max+1, r.max))
        self.intervals = sorted(result)       

    def minimum(self):
        if self.intervals:
            return self.intervals[0].min

    def count(self):
        total = 0
        for r in self.intervals:
            total += r.max - r.min + 1
        return total
        

# Example

def example():
    lines = """
5-8
0-2
4-7
""".strip().splitlines()
    admitted = RangeSet(Range(0, 9))
    for line in lines:
        line.strip()
        if line:
            print("exclude {}".format(line))
            min, max = line.split('-')
            excl = Range(int(min), int(max))
            admitted.exclude(excl)
    print(admitted)
    print("Lowest admissible value: {}".format(admitted.minimum()))
    print('= ' * 32)

# PART 1

def part1(lines):
    admitted = RangeSet(Range(0, MAXINT))
    for line in lines:
        line.strip()
        if line:
            print("exclude {}".format(line))
            min, max = line.split('-')
            excl = Range(int(min), int(max))
            admitted.exclude(excl)
    print(admitted)
    print("Lowest admissible value: {}".format(admitted.minimum()))
    print('= ' * 32)


    print("Total admitted IPs: {}".format(admitted.count()))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    # part2(lines)
