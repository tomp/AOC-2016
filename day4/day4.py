#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day {{ day }}
#
import re
from collections import namedtuple, defaultdict

INPUTFILE = 'input.txt'


name_re = re.compile(r"([a-z-]+)(\d+)\[([a-z]{5})\]")
EncryptedName = namedtuple('EncryptedRoom', ['name', 'sector_id', 'checksum'])

rooms = []
with open(INPUTFILE, 'r') as fp:
    for line in fp:
        m = name_re.match(line)
        if not m:
            raise ValueError("Bad input: '{}'".format(line.strip()))
        rooms.append(EncryptedName(*m.groups()))

# PART 1

real_rooms = []
sector_sum = 0
for room in rooms:
    count = defaultdict(int)
    stripped_name = room.name.replace('-', '')
    for char in stripped_name:
        count[char] += 1
    chars = sorted(count.keys(), key=lambda c:(-count[c], c))
    char_data = ", ".join(["{}:{}".format(c, count[c]) for c in chars])
    checksum = "".join(chars[:5])
    # print("'{}' <{}> [{}] -> [{}]".format(room.name, char_data, room.checksum, checksum))
    if checksum == room.checksum:
        real_rooms.append(room)
        sector_sum += int(room.sector_id)
    
print("{} real rooms found".format(len(real_rooms)))
print("Sector ID sum = {}".format(sector_sum))

print('- ' * 32)


# PART 2

def decrypted_name(encrypted_name, key):
    result = []
    for c in encrypted_name:
        if c == '-':
            result.append(c)
        else:
            i = ord('a') + (ord(c) - ord('a') + key) % 26
            result.append(chr(i))
    return "".join(result)

for room in real_rooms:
    real_name = decrypted_name(room.name, int(room.sector_id))
    print("{} \t[{}]".format(real_name, room.sector_id))

#print('- ' * 32)
