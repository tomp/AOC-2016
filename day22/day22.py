#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day N
#
import re
from heapq import heapify, heappop, heappush
from collections import namedtuple

DF_RE = re.compile(r"""
    node-x(\d+)-y(\d+)
    \s+(\d+)T
    \s+(\d+)T
    \s+(\d+)T
    """, re.VERBOSE)

Node = namedtuple('Node', ['x', 'y', 'size', 'used', 'avail'])

XSIZE, YSIZE = 32, 30

INPUTFILE = 'input.txt'

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

def parse_nodes(lines):
    """Parse information about the available nodes from
    the given lines of 'df' output.
    A list of Node objects is returned.
    """
    nodes = []
    for line in lines:
        m = DF_RE.search(line)
        if m:
            node = Node(*m.groups())
            nodes.append(Node(*m.groups()))
    assert(len(nodes) > 0)
    return nodes

class State(object):
    def __init__(self, nodes):
        self.xsize = 0
        self.ysize = 0
        self._size = []
        self._used = []
        self.history = []
        self._load_nodelist(nodes)
        self.goal = (self.xsize - 1, 0)

    def score(self):
        xg, yg = self.goal
        return len(self.history) + xg + yg

    def key(self):
        return (self.goal, tuple([tuple(row) for row in self._used]))

    def used(self, xy):
        x, y = xy
        return self._used[y][x]

    def avail(self, xy):
        x, y = xy
        return self._size[y][x] - self._used[y][x]

    def size(self, xy):
        x, y = xy
        return self._size[y][x]

    def _load_nodelist(self, nodes):
        xmax, ymax = 0, 0
        for node in nodes:
            x, y = int(node.x), int(node.y)
            if x > xmax:
                xmax = x
            if y > ymax:
                ymax = y
        self.ysize = ymax + 1
        self.xsize = xmax + 1
        for y in range(self.ysize):
            self._size.append([0] * self.xsize)
            self._used.append([0] * self.xsize)
        for node in nodes:
            x, y = int(node.x), int(node.y)
            self._size[y][x] = int(node.size)
            self._used[y][x] = int(node.used)

    def moves(self, teleport=False):
        """Return a list of moves available from the currnet state."""
        recv = [(self._size[y][x] - self._used[y][x], x, y)
                for x in range(self.xsize) for y in range(self.ysize)]
        recv.sort(reverse=True)
        send = [(self._used[y][x], x, y)
                for x in range(self.xsize) for y in range(self.ysize)
                if self._used[y][x] > 0]
        send.sort()
        # print("recv: {}...".format(str(recv[:5])))
        # print("send: {}...".format(str(send[:5])))
        moves = []
        for avail, x1, y1 in recv:
            for used, x0, y0 in send:
                if avail < used:
                    break
                if teleport or (x0 == x1 and abs(y0 - y1) == 1) or (
                                y0 == y1 and abs(x0 - x1) == 1):
                    self.apply((x0, y0), (x1, y1))
                    moves.append((self.score(), self.key(), list(self.history)))
                    self.undo()
        return moves

    def done(self):
        """Has the goal been met?"""
        return self.goal == (0, 0)

    def apply(self, xy0, xy1):
        """Move all data on node xy0 (x0, y0) to node xy1 (x1, y1).
        An exception is raised if the move is not possible.
        """
        x0, y0 = xy0
        x1, y1 = xy1
        data_size = self._used[y0][x0]
        assert(self._used[y1][x1] + data_size <= self._size[y1][x1])
        self.history.append((xy0, xy1, data_size))
        self._used[y1][x1] += data_size
        self._used[y0][x0] = 0
        if self.goal == xy0:
            self.goal = xy1

    def undo(self):
        """Undo the last data move."""
        if self.history:
            xy0, xy1, data_size = self.history.pop()
            x0, y0 = xy0
            x1, y1 = xy1
            self._used[y1][x1] -= data_size
            self._used[y0][x0] = data_size
            if self.goal == xy1:
                self.goal = xy0

    def reset(self):
        """Rewind the history, to restore this object to its original state.
        """
        while self.history:
            self.undo()

    def forward(self, history):
        """Rewind the history, and then apply the given moves."""
        self.reset()
        for xy0, xy1, _ in history:
            self.apply(xy0, xy1)


def search(state):
    """Find a series of moves that result in the goal data being
    moved to node (0, 0).

    The given state is modified in the course of the search, but will
    be restored to its original state when the search completes.

    A history of the required moves is returned.
    """
    visited = set(state.key())
    queue = state.moves()
    heapify(queue)
    total_states = 1
    while queue:
        score, key, path = heappop(queue)
        if key in visited:
            continue
        state.forward(path)
        print("[{}] score: {} goal:{}  moves:{}  (queue size {})".format(
            total_states, score, state.goal, len(path), len(queue)))
        if state.done():
            history = list(state.history)
            break
        visited.add(key)
        total_states += 1
        for move in state.moves():
            heappush(queue, move)

    state.reset()
    return history

        
# Example

def example():
    lines = """
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
""".splitlines()
    nodes = parse_nodes(lines)
    state = State(nodes)
    moves = state.moves()
    print("{} legal moves available in the initial state".format(len(moves)))
    for score, key, path in moves:
        xy0, xy1, data_size = path[-1]
        print("Move {} units from {} to {} ({} available)  score {}".format(
            state.used(xy0), str(xy0), str(xy1), state.avail(xy1), score))
    print('- ' * 32)

    path = search(state)
    print("Solution found in {} moves".format(len(path)))
    step = 0
    for xy0, xy1, data_size in path:
        step += 1
        print("step {:3d}: move {}T from {} to {}".format(step, data_size,
            str(xy0), str(xy1)))
    print('= ' * 32)

# PART 1

def part1(lines):
    nodes = parse_nodes(lines)
    state = State(nodes)
    moves = list(state.moves(teleport=True))
    print("{} teleport moves available in the initial state".format(
        len(moves)))
    assert(len(moves) == 952)
    print('- ' * 32)

    moves = list(state.moves())
    print("{} legal moves available in the initial state".format(len(moves)))
    for score, key, path in moves:
        xy0, xy1, data_size = path[-1]
        print("Move {} units from {} to {} ({} available)".format(
            state.used(xy0), str(xy0), str(xy1), state.avail(xy1)))
    print('= ' * 32)


# PART 2

def part2(lines):
    nodes = parse_nodes(lines)
    state = State(nodes)
    path = search(state)
    print("Solution found in {} moves".format(len(path)))
    step = 0
    for xy0, xy1, data_size in path:
        step += 1
        print("step {:3d}: move {}T from {} to {}".format(step, data_size,
            str(xy0), str(xy1)))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    # part2(lines)
