#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 13
#

def is_open(x, y, seed=0):
    """Return True if (x,y) is not a wall.  """
    val = x*(3 + x) + y*(y + 2*x + 1) + seed
    bits = bin(val).count('1')
    return (bits % 2 == 0)

def display(xmax, ymax, history, seed=0):
    """Return a string representation of the room layout in
    the range 0 <= x <= xmax and 0 <= y <= ymax.
    """
    head = " ".join([str(x%10) for x in range(xmax+1)])
    head = head.replace('0', '*')
    result = ["  "+head]
    for y in range(ymax+1):
        line = [str(y%10)]
        for x in range(xmax+1):
            if (x, y) in history:
                line.append('O')
            elif is_open(x, y, seed):
                line.append('.')
            else:
                line.append('#')
        line.append(str(y%10))
        result.append(" ".join(line))
    result.append("  "+head)
    return "\n".join(result)

def adjacent_cells(x, y, seed):
    """Generate the unvisited open cells adjacent to (x, y)."""
    for xn, yn in [(x-1,y), (x,y-1), (x+1,y), (x,y+1)]:
        if not visited(xn, yn) and is_open(xn, yn, seed):
            add_visit(xn, yn)
            yield (xn, yn)

# Track locations ("cells") visited in the search.
def reset_visits():
    global cells_visited
    cells_visited = set()
    cells_visited.add((0,0))
    cells_visited.add((0,1))

def add_visit(x, y):
    global cells_visited
    cells_visited.add((x, y))

def visited(x, y):
    global cells_visited
    return ((x, y) in cells_visited)

def dist(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def search(xgoal, ygoal, seed=0, x0=1, y0=1, max_steps=None):
    """Find the shortest path from (x0, y)) to (xgoal, ygoal).
    """
    reset_visits()
    add_visit(x0, y0)
    queue = [(1, x0, y0, [(x0, y0)])]
    total_visited = 0
    while queue:
        step, x, y, history = queue.pop(0)
        if max_steps is not None and step >= max_steps:
            break
        score = dist(x, y, xgoal, ygoal)
        # print("x={:2d}, y={:2d}: {} steps, dist={} ".format(x, y, step,
        #     score))
        # print(str(state))
        # print('- ' * 16)
        total_visited += 1
        if score == 0:
            break
        for xn, yn in adjacent_cells(x, y, seed):
            new_score = dist(xn, yn, xgoal, ygoal)
            queue.append((step+1, xn, yn, history + [(xn, yn)]))
    return history, total_visited


# Example

def example(seed=0):
    # print(display(9, 9, [], seed))
    # print('- ' * 32)
    history, total_visited = search(7, 4, seed)
    print(display(9, 9, history, seed))

    print('= ' * 32)

# PART 1

def part1(seed=0):
    history, total_visited = search(31, 39, seed)
    print(display(40, 45, history, seed))
    print("Path length: {}".format(len(history)))
    print("Total cells visited: {}".format(total_visited))
    print('= ' * 32)


# PART 2

def part2(seed):
    history, total_visited = search(31, 39, seed, max_steps=50)
    print(display(40, 45, list(cells_visited), seed))
    print("Path length: {}".format(len(history)))
    print("Total cells visited: {}".format(len(cells_visited)))
    print('= ' * 32)

if __name__ == '__main__':
    example(10)
    part1(1358)
    part2(1358)
