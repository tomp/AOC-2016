#!/usr/bin/env python3
#
#  Advent of Code 2016: Day 1
#
from collections import defaultdict

INFILE = "input.txt"
part = 2

with open(INFILE, 'r') as fp:
    steps = fp.read().split(', ')
print("{} steps".format(len(steps)))

# directions 0:N, 1:E, 2:S, 3:W
dir = 0
x = 0
y = 0

dir_str = ['N', 'E', 'S', 'W']

def new_dir(dir, turn):
    """Return direction (0-3) after turning left or right.
    dir ... the initial direction (integer 0-3)
    turn .. 'R" or 'L'.
    """
    if turn == 'R':
        return (dir + 1) % 4
    else:
        return (dir - 1) % 4

def walk(xinit, yinit, dirinit, steps, part2=False):
    x, y, dir = xinit, yinit, dirinit
    visited = defaultdict(int)
    visited[(x,y)] += 1

    print("Start: ({:3d}, {:3d}) {}".format(x, y, dir_str[dir]))
    for idx, step in enumerate(steps):
        turn, dist = step[0], int(step[1:])
        x0, y0 = x, y
        dir0 = dir
        dir = new_dir(dir, turn)
        print("{:2d}: ({:3d}, {:3d}) {} -- {} {} --> ".format(
            idx+1, x0, y0, dir_str[dir0], turn, dist), end="")
        if dir == 0:
            for dy in range(1, dist+1):
                if part2 and visited[(x, y+dy)]:
                    return(x,y+dy)
                visited[(x, y+dy)] += 1
            y += dist
        elif dir == 1:
            for dx in range(1, dist+1):
                if part2 and visited[(x+dx, y)]:
                    return(x+dx,y)
                visited[(x+dx, y)] += 1
            x += dist
        elif dir == 2:
            for dy in range(1, dist+1):
                if part2 and visited[(x, y-dy)]:
                    return(x,y-dy)
                visited[(x, y-dy)] += 1
            y -= dist
        elif dir == 3:
            for dx in range(1, dist+1):
                if part2 and visited[(x-dx, y)]:
                    return(x-dx,y)
                visited[(x-dx, y)] += 1
            x -= dist
        else:
            raise ValueError("x,y: ({}, {})  dir: {}  turn, dist: {} {}".format(
                x, y, dir_str[dir], turn, dist))
        print("({:3d}, {:3d}) {}".format(x, y, dir_str[dir]))
    return(x, y)

xfinal, yfinal = walk(x, y, dir, steps, False)
print("Final: ({:3d}, {:3d})".format(xfinal,yfinal))
print('- ' * 32)

xfinal, yfinal = walk(x, y, dir, steps, True)
print("Final: ({:3d}, {:3d})".format(xfinal,yfinal))
print('- ' * 32)
