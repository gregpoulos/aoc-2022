#!/usr/local/bin/python3

def rangify(s):
  return [int(x) for x in s.split('-')]

def contains(r1, r2):
  return (r1[0] <= r2[0]) and (r1[1] >= r2[1])

counter = 0
for line in open('input.txt', 'r').readlines():
  a, b = [rangify(s) for s in line.strip().split(',')]
  if contains(a, b) or contains(b, a):
    counter += 1

print(counter)
