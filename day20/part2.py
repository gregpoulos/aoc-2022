#!/usr/local/bin/python3

import sys

KEY = 811589153

fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]

class Node(object):
  def __init__(self, val=0, base=0, left=None, right=None):
    self.val = val
    self.base = base
    self.left = left
    self.right = right

  def __str__(self):
    return f'{{ {self.val} % {self.base} | right={self.right.val if self.right else "X"} | left={self.left.val if self.left else "X"}}}'

  def print_chain(self):
    here = self
    while here.right != self:
      print(here)
      here = here.right
    print(here)

  def insert_right(self, to_insert):
    to_insert.right = self.right
    self.right.left = to_insert
    self.right = to_insert
    to_insert.left = self

  def remove(self):
    right = self.right
    left = self.left
    right.left = left
    left.right = right

  def get_neighbor(self, steps):
    pointer = self
    while steps > 0:
      pointer = pointer.right
      steps -= 1
    while steps < 0:
      pointer = pointer.left
      steps += 1
    return pointer

  def mix(self):
    mod = self.val % (self.base - 1)
    if mod == 0: return
    self.remove()
    self.get_neighbor(mod).insert_right(self)

def chain_from_list(vals):
  base = len(vals)
  first_node = Node(val=vals[0], base=base)
  ranks = [first_node]
  for i, val in enumerate(vals[1:]):
    n = Node(val=val, base=base, left=ranks[i])
    ranks[i].right = n
    ranks.append(n)
  ranks[-1].right = ranks[0]
  ranks[0].left   = ranks[-1]
  return ranks

def mix(ranks):
  for node in ranks:
    node.mix()

with open(fn, 'r') as f:
  vals = [int(i)*KEY for i in f.read().strip().split('\n')]

# construct chain
ranks = chain_from_list(vals)
zero_node = next(n for n in ranks if n.val == 0)

for _ in range(10):
  mix(ranks)
a = zero_node.get_neighbor(1000)
b = a.get_neighbor(1000)
c = b.get_neighbor(1000)
print(f'{a.val} + {b.val} + {c.val} = {a.val+b.val+c.val}')
