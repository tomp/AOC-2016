#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 5
#
import hashlib
from itertools import count

INPUT = 'ugkcyxxp'

# PART 1

def next_char(door_id, start=0):
    for idx in count(start):
        text = "{}{}".format(door_id, idx).encode()
        hashi = hashlib.md5(text).hexdigest()
        if hashi.startswith('00000'):
            return (hashi[5], idx)

def next_char2(door_id, start=0):
    for idx in count(start):
        text = "{}{}".format(door_id, idx).encode()
        hashi = hashlib.md5(text).hexdigest()
        if hashi.startswith('00000'):
            return (hashi[6], hashi[5], idx)

pwd = []
idx = -1
for i in range(8):
    c, idx = next_char(INPUT, idx+1)
    print("char: {}  idx: {}".format(c, idx))
    pwd.append(c)
print("DoorID: {}  Password: {}".format(INPUT, "".join(pwd)))

print('- ' * 32)


# PART 2

VALID_POS = '01234567'

pwd2 = [' '] * 8
idx = -1
while ' ' in pwd2:
    c, pos, idx = next_char2(INPUT, idx+1)
    print("char: {}  pos: {}  idx: {}".format(c, pos, idx))
    if pos in VALID_POS and pwd2[int(pos)] == ' ':
        pwd2[int(pos)] = c
    else:
        print("-- INVALID")
print("DoorID: {}  Password: {}".format(INPUT, "".join(pwd2)))

print('- ' * 32)
