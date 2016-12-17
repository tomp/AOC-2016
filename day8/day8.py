#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 8
#
import re

INPUTFILE = 'input.txt'

WIDTH = 50
HEIGHT = 6

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

class Display(object):
    PIXEL_OFF = '.'
    PIXEL_ON = '#'

    rect_re = re.compile(r"rect (\d+)x(\d+)")
    rotate_column_re = re.compile(r"rotate column x=(\d+) by (\d+)")
    rotate_row_re = re.compile(r"rotate row y=(\d+) by (\d+)")

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.disp = [[self.PIXEL_OFF for x in range(width)] for y in range(height)]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "\n".join(["".join(row) for row in self.disp])

    def rect(self, w, h):
        assert(w <= self.width)
        assert(h <= self.height)
        for y in range(h):
            for x in range(w):
                self.disp[y][x] = self.PIXEL_ON

    def rotate_row(self, y, n):
        assert(y <= self.height)
        n = n % self.width
        self.disp[y] = self.disp[y][-n:] + self.disp[y][:-n]

    def rotate_column(self, x, n):
        assert(x <= self.width)
        n = n % self.height
        col = [self.disp[y][x] for y in range(self.height)]
        col = col[-n:] + col[:-n]
        for y in range(self.height):
            self.disp[y][x] = col[y]

    def pixels(self):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.disp[y][x] == self.PIXEL_ON:
                    count += 1
        return count

    def execute(self, cmd):
        m = self.rect_re.match(cmd)
        if m:
            w, h = m.groups()
            self.rect(int(w), int(h))
            return
        m = self.rotate_column_re.match(cmd)
        if m:
            x, n = m.groups()
            self.rotate_column(int(x), int(n))
            return
        m = self.rotate_row_re.match(cmd)
        if m:
            y, n = m.groups()
            self.rotate_row(int(y), int(n))
            return
            
# Example

def example():
    disp = Display(7,3)
    disp.rect(3,2)
    disp.rotate_column(1,1)
    disp.rotate_row(0,4)
    disp.rotate_column(1,1)
    print(disp)
    print("{} pixels lit".format(disp.pixels()))

# PART 1

def part1(lines):
    disp = Display(WIDTH, HEIGHT)
    for line in lines:
        disp.execute(line)
    print(disp)
    print("{} pixels lit".format(disp.pixels()))
        
    print('- ' * 32)


# PART 2

def part2():
    print('- ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    part2()
