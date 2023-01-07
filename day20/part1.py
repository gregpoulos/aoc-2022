#!/usr/local/bin/python3

import sys

fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]

class Node(object):
  def __init__(self, val=0, left=None, right=None):
    super(Node, self).__init__()
    self.val = val
    self.left = left
    self.right = right

  def __str__(self):
    return f'{{ val={self.val} | right={self.right.val if self.right else "X"} | left={self.left.val if self.left else "X"}}}'

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

  def insert_left(self, to_insert):
    self.left.insert_right(to_insert)

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
    if self.val == 0: return
    self.remove()
    other = self.get_neighbor(self.val)
    if self.val < 0:
      other.insert_left(self)
    else:
      other.insert_right(self)

def chain_from_list(lst):
  first_node = Node(val=lst[0])
  ranks = [first_node]
  for i, val in enumerate(lst[1:]):
    n = Node(val=val, left=ranks[i])
    ranks[i].right = n
    ranks.append(n)
  ranks[-1].right = ranks[0]
  ranks[0].left   = ranks[-1]
  return ranks

def mix(ranks):
  for node in ranks:
    node.mix()

with open(fn, 'r') as f:
  inputs = [int(i) for i in f.read().strip().split('\n')]

# construct chain
ranks = chain_from_list(inputs)
zero_node = next(n for n in ranks if n.val == 0)

mix(ranks)
a = zero_node.get_neighbor(1000)
b = a.get_neighbor(1000)
c = b.get_neighbor(1000)
print(f'{a.val} + {b.val} + {c.val} = {a.val+b.val+c.val}')
