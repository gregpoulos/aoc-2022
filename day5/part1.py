#!/usr/local/bin/python3

import re

stacks = [
  [],
  ['Q', 'F', 'M', 'R', 'L', 'W', 'C', 'V'],
  ['D', 'Q', 'L'],
  ['P', 'S', 'R', 'G', 'W', 'C', 'N', 'B'],
  ['L', 'C', 'D', 'H', 'B', 'Q', 'G'],
  ['V', 'G', 'L', 'F', 'Z', 'S'],
  ['D', 'G', 'N', 'P'],
  ['D', 'Z', 'P', 'V', 'F', 'C', 'W'],
  ['C', 'P', 'D', 'M', 'S'],
  ['Z', 'N', 'W', 'T', 'V', 'M', 'P', 'C'],
]

for line in open('input.txt', 'r').readlines():
  n, source, dest = [int(x) for x in re.findall(r'\d+', line)]
  for _ in range(n):
    val = stacks[source].pop()
    stacks[dest].append(val)

print(''.join([stack.pop() for stack in stacks[1:10]]))
