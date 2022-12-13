#!/usr/local/bin/python3
from ast import literal_eval

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

ps = [literal_eval(line) for line in open('input.txt', 'r').readlines() if line != '\n']
# d1 = [[2]]
# d2 = [[6]]
# ps.append(d1)
# ps.append(d2)

out = 0
for i in range(len(ps)//2):
  if compare_lists(ps[2*i], ps[2*i+1]) > 0:
    out += (i+1)
print(out)
