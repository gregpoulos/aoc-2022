#!/usr/local/bin/python3

def rangify(s):
  return [int(x) for x in s.split('-')]

def overlaps(r1, r2):
  # ensure r1 is always the "earlier" range
  if r2[0] < r1[0]:
    return overlaps(r2, r1)
  return r1[1] >= r2[0]

counter = 0
for line in open('input.txt', 'r').readlines():
  a, b = [rangify(s) for s in line.strip().split(',')]
  if overlaps(a, b):
    counter += 1

print(counter)
