#!/usr/local/bin/python3

elves = []
elf = []
elves.append(elf)

for line in open('calories.txt', 'r').readlines():
    if line == '\n':
        elf = []
        elves.append(elf)
    else:
        elf.append(int(line))

print(sum(sorted([sum(elf) for elf in elves])[-3:]))
