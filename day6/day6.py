#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 6
#
from collections import defaultdict

INPUTFILE = 'input.txt'

lines = []
with open(INPUTFILE, 'r') as fp:
    for line in fp:
        line = line.strip()
        if line:
            lines.append(line)

nchar = len(lines[0])

# PART 1

def message_from_stats(count, modified=False):
    message = []
    for idx, freq in enumerate(count):
        chars = sorted(freq.keys(), key=lambda c: freq[c], reverse=True)
        # print("Char {}:  {}".format(idx, ", ".join(
        #     ["'{}':{}".format(c, freq[c]) for c in chars])))
        if modified:
            message.append(chars[-1])
        else:
            message.append(chars[0])
    return "".join(message)

count = []
for idx in range(nchar):
    count.append(defaultdict(int))

for line in lines:
    for idx, c in enumerate(line):
        count[idx][c] += 1
    # print("## '{}'".format(line))
    message = message_from_stats(count)
    # print(">> '{}\n".format(message))

print("Message: '{}'".format("".join(message)))


print('- ' * 32)


# PART 2

message = message_from_stats(count, modified=True)

print("Message: '{}'".format("".join(message)))

print('- ' * 32)
