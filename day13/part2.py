#!/usr/local/bin/python3
from ast import literal_eval
from functools import cmp_to_key

def compare_ints(i1, i2):
  return i2 - i1

def compare_lists(l1, l2):
  out = 0
  for v1, v2 in zip(l1, l2):
    if type(v1) == int and type(v2) == int:
      out = compare_ints(v1, v2)
    elif type(v1) == int:
      out = compare_lists([v1], v2)
    elif type(v2) == int:
      out = compare_lists(v1, [v2])
    else:
      out = compare_lists(v1, v2)
    if out != 0:
      return out
  else:
    return compare_ints(len(l1), len(l2))

def compare_packets(p1, p2):
  return compare_lists(p1, p2)*-1

d1, d2, d1i, d2i = [[2]], [[6]], 0, 0
ps = [literal_eval(line) for line in open('input.txt', 'r').readlines() if line != '\n']
ps.append(d1)
ps.append(d2)

for i, p in zip(range(1, len(ps)+1), sorted(ps, key=cmp_to_key(compare_packets))):
  if p == d1: d1i = i
  if p == d2: d2i = i
print(d1i*d2i)
