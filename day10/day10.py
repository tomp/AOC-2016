#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 10
#
import re

INPUTFILE = 'input.txt'

def load_input(infile):
    lines = []
    with open(infile, 'r') as fp:
        for line in fp:
            line = line.strip()
            if line:
                lines.append(line)
        return lines

distribute_re = re.compile(r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")
assign_re = re.compile(r"value (\d+) goes to bot (\d+)")

_bots = {}
output = {}

def init_bots():
    global _bots, output
    _bots = {}
    output = {}

def bot(number):
    """Bot factory"""
    if not number in _bots:
        _bots[number] = Bot(number)
    return _bots[number]

def bot_numbers():
    return sorted(_bots.keys())

def execute_rule(rule):
    """Execute the given rule."""
    if len(rule.strip()) == 0:
        return
    m = assign_re.match(rule)
    if m:
        value, number = m.groups()
        bot(int(number)).assign(int(value))
        return
    m = distribute_re.match(rule)
    if m:
        number, low_type, low_num, high_type, high_num = m.groups()
        bot(int(number)).distributes(low_type, int(low_num), high_type, int(high_num))
        return
    raise ValueError("Unrecognized rule: {}".format(rule))


class Bot(object):
    def __init__(self, number):
        self.number = number
        self.low = None   # number of bot receiving our low-valued chip
        self.high = None  # number of bot receiving our high-valued chip
        self.values = []  # our chip values
    
    def configured(self):
        return len(self.values) == 2 and self.low is not None and self.high is not None

    def assign(self, value):
        self.values.append(int(value))
        # print("Assign value {} to bot {}".format(value, self.number))
        if self.configured():
            self._distribute()
            
    def distributes(self, low_type, low_num, high_type, high_num):
        self.low_type = low_type
        self.low = int(low_num)
        self.high_type = high_type
        self.high = int(high_num)
        if self.configured():
            self._distribute()

    def _distribute(self):
        self.values.sort()
        low_value, high_value = self.values
        if self.low_type == 'bot':
            bot(self.low).assign(low_value)
        else:
            output[self.low] = low_value
        if self.high_type == 'bot':
            bot(self.high).assign(high_value)
        else:
            output[self.high] = high_value

# Example

def example():
    rules = """
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
""".split("\n")
    init_bots()
    for rule in rules:
        execute_rule(rule)
    
    for number in sorted(output.keys()):
        print("output {} contains value-{} microchip".format(
            number, output[number]))
    for number in bot_numbers():
        print("bot {} compares value-{} and value-{} microchips".format(
            number, *bot(number).values))
    print('- ' * 32)
    

# PART 1

def part1(rules):
    init_bots()
    for rule in rules:
        execute_rule(rule)
    
    for number in bot_numbers():
        if bot(number).values == [17, 61]:
            print("bot {} compares value-{} and value-{} microchips".format(
                number, *bot(number).values))
    print('- ' * 32)


# PART 2

def part2():
    product = 1
    for number in range(3):
        print("output {} contains value-{} microchip".format(
            number, output[number]))
        product *= output[number]
    print("The product of the microchip values is {}".format(product))
    print('- ' * 32)

if __name__ == '__main__':
    example()
    lines = load_input(INPUTFILE)
    part1(lines)
    part2()
