#!/usr/bin/env python3
#
#  Advent of Code 2016 - Day 7
#
import re

INPUTFILE = 'input.txt'

lines = []
with open(INPUTFILE, 'r') as fp:
    for line in fp:
        line = line.strip()
        if line:
            lines.append(line)

# PART 1

abba_re = re.compile(r"([a-z])([a-z])\2\1")
hypernet_re = re.compile(r"\[[^\]]*\]")

def hypernets(ip):
    return hypernet_re.findall(ip)

def supernets(ip):
    return hypernet_re.split(ip)

def first_abba(text):
    m = abba_re.search(text)
    if not m:
        return ""
    abba = m.group(0)
    if abba[0] == abba[1]:
        return ""
    return abba

def is_tls(line):
    if any([first_abba(seq) for seq in hypernets(line)]):
        return False
            
    if any([first_abba(seq) for seq in supernets(line)]):
        return True

tls = [line for line in lines if is_tls(line)]

print("{} IPs support TLS".format(len(tls)))
print('- ' * 32)


# PART 2

aba_re = re.compile(r"([a-z])([a-z])\1")

def all_aba(text):
    # print("\ntext: '{}'".format(text))
    result = []
    pos = 0
    m = aba_re.search(text[pos:])
    while m:
        aba = m.group(0)
        # print("...found {} @ {}".format(aba, pos + m.start()))
        if aba[0] != aba[1]:
            yield aba
        pos += m.start() + 1
        m = aba_re.search(text[pos:])

def is_ssl(line):
    hypers = hypernets(line)
    for super in supernets(line):
        for aba in all_aba(super):
            bab = aba[1] + aba[0] + aba[1]
            if any([bab in hyper for hyper in hypers]):
                return True
    return False

ssl = [line for line in lines if is_ssl(line)]
print("{} IPs support SSL".format(len(ssl)))
                

print('- ' * 32)
