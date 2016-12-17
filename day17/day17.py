#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day N
#
from hashlib import md5

INPUT = 'pgflpeqp'

XSIZE = 4
YSIZE = 4

OPEN_CODES = 'bcdef'

def open_doors(passcode, history=[], x=0, y=0):
    """Calculate the state (open or closed) for each door in the room
    that was arrived at by the given history.

    The history is a list of characters ('U', 'D', 'R', 'L') recording
    the direction travelled on each step through the maze, starting at
    location (0, 0).

    No input arguments are modified.

    The return value is the list of open doors ('UDLR').
    """
    result = []
    input = passcode + "".join(history)
    hash = md5(input.encode()).hexdigest()[:4]
    if hash[0] in OPEN_CODES and y > 0:
        result.append('U')
    if hash[1] in OPEN_CODES and y < YSIZE-1:
        result.append('D')
    if hash[2] in OPEN_CODES and x > 0:
        result.append('L')
    if hash[3] in OPEN_CODES and x < XSIZE-1:
        result.append('R')
    return result

def position(history, x0=0, y0=0):
    """Return the (x, y) coords of the room to which the given
    path leads, from the specified initial position.
    """
    x, y = x0, y0
    for d in history:
        if d == 'U':
            y -= 1
        elif d == 'D':
            y += 1
        elif d == 'L':
            x -= 1
        elif d == 'R':
            x += 1
        else:
            raise ValueError("Illegal direction '{}' in history '{}'".format(
               d,  "-".join(history)))
    return (x, y)

def search(passcode, shortest_path=True):
    """Find the shortest or longest path to the vault entrance (position 4,4).
    The path is returned as a list of directions ('UDLR').
    """
    # print("\npasscode: {}'".format(passcode))
    step, x, y = 0, 0, 0
    history = []
    queue = [(step, x, y, list(history))]
    solutions = []
    while queue:
        step, x, y, history = queue.pop(0)
        if x == XSIZE - 1 and y == YSIZE - 1:
            if shortest_path:
                break
            else:
                solutions.append(history)
                continue
        doors = open_doors(passcode, history, x, y)
        # print("[{}] ({}, {}) {} -> {}".format(step, x, y,
        #     "".join(history), ", ".join(doors)))
        for d in doors:
            x1, y1 = position([d], x, y)
            queue.append((step+1, x1, y1, history + [d]))
            # print("  {} --> ({}, {}) {}".format(d, x1, y1,
            #     "".join(history)+d))
    if shortest_path:
        return history
    else:
        return solutions


# Example

def example():
    passcode = 'hijkl'
    history = []
    expected = 'D'
    dirs = open_doors(passcode)
    print("passcode: '{}'  history: '{}' --> {}".format(passcode,
        "-".join(history), ", ".join(dirs)))
    assert("".join(dirs) == expected)

    history.append(dirs[0])
    x, y = position(history)
    expected = 'UR'
    dirs = open_doors(passcode, history, x, y)
    print("passcode: '{}'  history: '{}' --> {}".format(passcode,
        "-".join(history), ", ".join(dirs)))
    assert("".join(dirs) == expected)

    SHORTEST_PATH_CASES = [
        ('ihgpwlah', 'DDRRRD'),
        ('kglvqrro', 'DDUDRLRRUDRD'),
        ('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR')]

    for passcode, expected in SHORTEST_PATH_CASES:
        history = search(passcode)
        path = "".join(history)
        steps = len(history)
        print("passcode: '{}' shortest path {} steps: {}".format(passcode,
            steps, path))
        assert(path == expected)

    LONGEST_PATH_CASES = [
        ('ihgpwlah', 370),
        ('kglvqrro', 492),
        ('ulqzkmiv', 830)]

    for passcode, expected in LONGEST_PATH_CASES:
        solutions = search(passcode, shortest_path=False)
        steps = len(solutions[-1])
        print("passcode: '{}' longest path: {} steps".format(passcode, steps))
        assert(steps == expected)
    print('= ' * 32)

# PART 1

def part1(passcode):
    history = search(passcode)
    path = "".join(history)
    steps = len(history)
    print("passcode: '{}' shortest path: {} steps: {}".format(passcode,
        steps, path))
    print('= ' * 32)


# PART 2

def part2(passcode):
    solutions = search(passcode, shortest_path=False)
    steps = len(solutions[-1])
    print("passcode: '{}' longest path: {} steps".format(passcode, steps))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    part1(INPUT)
    part2(INPUT)
