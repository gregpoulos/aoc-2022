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

ps = [literal_eval(line) for line in open('input.txt', 'r').readlines() if line != '\n']
d1 = [[2]]
d2 = [[6]]
ps.append(d1)
ps.append(d2)

i = 0
d1i = 0
d2i = 0
for p in sorted(ps, key=cmp_to_key(compare_packets)):
  i += 1
  if p == d1: d1i = i
  if p == d2: d2i = i
print(d1i*d2i)
