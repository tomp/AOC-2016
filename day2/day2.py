#!/usr/bin/env python3
#
#  Advent of Code 2016: Day 2
#

INFILE = "input.txt"

with open(INFILE, 'r') as fp:
    button_seq = [line.strip() for line in fp.readlines()]

layout1 = [[None, None, None, None, None],
           [None,  '1',  '2',  '3', None],
           [None,  '4',  '5',  '6', None],
           [None,  '7',  '8',  '9', None],
           [None, None, None, None, None]]

layout2 = [[None, None, None, None, None, None, None],
           [None, None, None,  '1', None, None, None],
           [None, None,  '2',  '3',  '4', None, None],
           [None,  '5',  '6',  '7',  '8',  '9', None],
           [None, None,  'A',  'B',  'C', None, None],
           [None, None, None,  'D', None, None, None],
           [None, None, None, None, None, None, None]]

def button_at(x, y, layout):
    return layout[y][x]

def next_position(xinit, yinit, layout, seq):
    x, y = xinit, yinit

    print("Start: ({:3d}, {:3d}) {}".format(x, y, button_at(x,y,layout)))
    for idx, dir in enumerate(seq):
        x0, y0 = x, y
        print("{:2d}: ({:3d}, {:3d}) {} -- {} --> ".format(
            idx, x0, y0, button_at(x0, y0, layout), dir), end="")
        if dir == 'U':
            y = y - 1
        elif dir == 'D':
            y = y + 1
        elif dir == 'R':
            x = x + 1
        elif dir == 'L':
            x = x - 1
        else:
            raise ValueError("x,y: ({}, {})  {}  dir: '{}'".format(
                x, y, button_at(x,y, layout), dir))
        if button_at(x, y, layout) is None:
            x, y = x0, y0
        print("({:3d}, {:3d}) {}".format(x, y, button_at(x, y, layout)))
    return(x, y)


if __name__ == '__main__':
    pos1 = []
    x, y = 2, 2
    for idx, seq in enumerate(button_seq):
        x, y = next_position(x, y, layout1, seq)
        pos1.append((x, y))
        print("Button #{}: {} ({:3d}, {:3d})".format(idx+1,
            button_at(x, y, layout1), x, y))
        print('- ' * 32)

    pos2 = []
    x, y = 1, 3
    for idx, seq in enumerate(button_seq):
        x, y = next_position(x, y, layout2, seq)
        pos2.append((x, y))
        print("Button #{}: {} ({:3d}, {:3d})".format(idx+1,
            button_at(x, y, layout2), x, y))
        print('- ' * 32)

