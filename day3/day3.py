#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 3
#
INPUTFILE = 'input.txt'

triples = []
with open(INPUTFILE, 'r') as fp:
    for line in fp:
        triples.append([int(v) for v in line.strip().split()])

count = 0
for row in triples:
    a, b, c = sorted(row)
    if a + b > c:
        count += 1
        print("OK {} {} ({}) {}".format(a, b, a + b, c))
    else:
        print("!! {} {} ({}) {}".format(a, b, a + b, c))

print("Possible triangles: {}".format(count))
print('- ' * 32)

vals = list([row[0] for row in triples] + 
             [row[1] for row in triples] + 
             [row[2] for row in triples])
triples2 = zip(vals[0::3], vals[1::3], vals[2::3])

count = 0
for row in triples2:
    a, b, c = sorted(row)
    if a + b > c:
        count += 1
        print("OK {} {} ({}) {}".format(a, b, a + b, c))
    else:
        print("!! {} {} ({}) {}".format(a, b, a + b, c))

print("Possible triangles: {}".format(count))
print('- ' * 32)
