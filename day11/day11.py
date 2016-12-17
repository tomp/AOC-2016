#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 11
#
from collections import namedtuple
from itertools import combinations
from heapq import heapify, heappush, heappop

INPUTFILE = 'input.txt'

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

def reset_visits():
    global states_visited
    states_visited = set()

def add_visit(state):
    global states_visited
    states_visited.add(hash(state))

def visited(state):
    global states_visited
    return (hash(state) in states_visited)


# Data structure for BFS
SearchNode = namedtuple("SearchNode", ['distance', 'steps', 'score', 'state', 'history'])


class State(object):
    FLOORS = 4

    def __init__(self, elevator, generators, chips):
        assert(len(generators) == len(self.ISOTOPES))
        assert(len(chips) == len(self.ISOTOPES))
        self.elevator = elevator
        self.generators = list(generators)
        self.chips = list(chips)
    
    def __str__(self):
        lines = []
        for idx in range(self.FLOORS):
            floor = self.FLOORS - idx
            elev = 'E ' if self.elevator == floor else ". "
            parts = [elev]
            for iso, gen in enumerate(self.generators):
                if gen == floor:
                    parts.append(self.ISOTOPES[iso] + 'G')
                else:
                    parts.append(". ")
                if self.chips[iso] == floor:
                    parts.append(self.ISOTOPES[iso] + 'M')
                else:
                    parts.append(". ")
            line = "F{} {}".format(floor, " ".join(parts))
            lines.append(line)
        return "\n".join(lines)

    def __lt__(self, other):
        return self.score() < other.score()

    def __hash__(self):
        # values = [self.elevator] + self.generators + self.chips
        values = [self.elevator] + sorted(zip(self.generators, self.chips))
        return hash(tuple(values))

    def clone(self):
        return self.__class__(self.elevator, self.generators, self.chips)

    def score(self):
        result = 0
        for iso in range(len(self.ISOTOPES)):
            result += self.FLOORS - self.generators[iso]
            result += self.FLOORS - self.chips[iso]
        return result
    
    def next_states(self):
        if self.elevator == self.FLOORS:
            new_floors = [self.elevator - 1]
        elif self.elevator == 1:
            new_floors = [self.elevator + 1]
        else:
            new_floors = [self.elevator + 1, self.elevator - 1]
        for new_floor in new_floors:
            all_generators, all_chips, shielded_chips = self.on_floor()
            for iso in shielded_chips:
                new_state = self.clone()
                new_state.elevator = new_floor
                new_state.generators[iso] = new_floor
                new_state.chips[iso] = new_floor
                if not visited(new_state):
                    add_visit(new_state)
                    if not new_state.fried():
                        yield new_state
            for iso1, iso2 in combinations(all_chips, 2):
                new_state = self.clone()
                new_state.elevator = new_floor
                new_state.chips[iso1] = new_floor
                new_state.chips[iso2] = new_floor
                # print("Move chips {} & {} to floor {}".format(iso1, iso2,
                #     new_floor))
                # print(new_state)
                if not visited(new_state):
                    add_visit(new_state)
                    if not new_state.fried():
                        yield new_state
            for iso1, iso2 in combinations(all_generators, 2):
                new_state = self.clone()
                new_state.elevator = new_floor
                new_state.generators[iso1] = new_floor
                new_state.generators[iso2] = new_floor
                if not visited(new_state):
                    add_visit(new_state)
                    if not new_state.fried():
                        yield new_state
            for iso in all_chips:
                new_state = self.clone()
                new_state.elevator = new_floor
                new_state.chips[iso] = new_floor
                # print("Move chip {} to floor {}".format(iso, new_floor))
                # print(new_state)
                if not visited(new_state):
                    add_visit(new_state)
                    if not new_state.fried():
                        yield new_state
            for iso in all_generators:
                new_state = self.clone()
                new_state.elevator = new_floor
                new_state.generators[iso] = new_floor
                if not visited(new_state):
                    add_visit(new_state)
                    if not new_state.fried():
                        yield new_state
        

    def fried(self):
        for floor in range(1, self.FLOORS+1):
            if self.unshielded_chips(floor) and floor in self.generators:
                return True

    def on_floor(self, floor=None):
        if floor is None:
            floor = self.elevator
        all_gen = [iso for iso, gen in enumerate(self.generators)
                if gen == floor]
        all_chip = [iso for iso, chip in enumerate(self.chips)
                if chip == floor]
        shielded = [iso for iso in all_chip if self.generators[iso] == floor]
        return all_gen, all_chip, shielded

    def shielded_chips(self, floor):
        return [iso for iso, chip in enumerate(self.chips)
                if chip == floor and self.generators[iso] == floor]

    def unshielded_chips(self, floor):
        return [iso for iso, chip in enumerate(self.chips)
                if chip == floor and self.generators[iso] != floor]

    def bounds_check(self):
        if self.elevator < 1 or self.elevator > self.FLOORS:
            return False
        for chip in self.chips:
            if chip < 1 or chip > self.FLOORS:
                return False
        for gen in self.generators:
            if gen < 1 or gen > self.FLOORS:
                return False

class State2(State):
    ISOTOPES = ['H', 'L']

class State5(State):
    ISOTOPES = ['P', 'Q', 'R', 'S', 'T']

class State7(State):
    ISOTOPES = ['P', 'Q', 'R', 'S', 'T', 'D', 'E']
            

def search(initial_state):
    reset_visits()
    add_visit(initial_state)
    score = initial_state.score()
    queue = []
    heappush(queue, SearchNode(score, 0, score, initial_state,
        [initial_state]))
    states = 0
    while queue:
        states += 1
        rank, step, score, state, history = heappop(queue)
        # print("Steps: {}  Score: {}".format(step, score))
        # print(str(state))
        # print('- ' * 16)
        if state.score() == 0:
            break
        for new_state in state.next_states():
            new_score = new_state.score()
            heappush(queue, SearchNode(step + new_score + 1, step + 1,
                new_score, new_state, history + [new_state]))
    return history, states


def example():
    state = State2(1, [2, 3], [1, 1])
    history, states = search(state)
    print('= ' * 16)
    for step, state in enumerate(history):
        print("Step: {}  (score {})".format(step, state.score()))
        print(str(state))
        print('- ' * 16)
    print("## {} states considered".format(states))
    print('= ' * 32)

# PART 1

def part1():
    state = State5(1, [1, 3, 3, 1, 1], [2, 3, 3, 2, 1])
    history, states = search(state)
    print('= ' * 16)
    for step, state in enumerate(history):
        print("Step: {}  (score {})".format(step, state.score()))
        print(str(state))
        print('- ' * 16)
    print("## {} states considered".format(states))
    print('= ' * 32)


# PART 2

def part2():
    state = State7(1, [1, 3, 3, 1, 1, 1, 1], [2, 3, 3, 2, 1, 1, 1])
    history, states = search(state)
    print('= ' * 16)
    for step, state in enumerate(history):
        print("Step: {}  (score {})".format(step, state.score()))
        print(str(state))
        print('- ' * 16)
    print("## {} states considered".format(states))
    print('= ' * 32)

if __name__ == '__main__':
    example()
    part1()
    part2()
