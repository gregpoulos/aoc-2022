#!/usr/local/bin/python3

def get_priority(item):
  x = ord(item)
  if 97 <= x <= 122:
    return x - 96
  else:
    return x - 38

def find_dupe(rucksack):
  half = len(rucksack) // 2
  s = set(rucksack[:half]).intersection(set(rucksack[half:]))
  return list(s)[0]

groups = []
group = []
counter = 0
for line in open('rucksacks.txt', 'r').readlines():
  group.append(line.strip())
  counter += 1
  if counter % 3 == 0:
    groups.append(group)
    group = []

total = 0
for group in groups:
  sets = [set(x) for x in group]
  badge = list(sets[0].intersection(sets[1]).intersection(sets[2]))[0]
  total += get_priority(badge)

print(total)

# total += get_priority(find_dupe(line.strip()))
