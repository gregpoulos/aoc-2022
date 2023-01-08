#!/usr/local/bin/python3

import re
import sys

class Node(object):
  """docstring for Node"""
  def __init__(self, name, value=None, left=None, right=None):
    self.name = name
    if re.match(r"[0-9]+", value): 
      self.value = int(value)
      self.left = self.right = None
    else:
      m = re.search(r'[\+\-\*/]', value)
      self.value = m.group()
      self.left, self.right = re.findall(r'[a-z]{4}', value)[:2]

  def __str__(self):
    if self.is_leaf():
      return f'{{ {self.value} }}'
    else:
      return f'{{ {self.left.name} {self.value} {self.right.name} }}'

  def is_leaf(self):
    return not self.left and not self.right

  def op(self):
    if self.is_leaf(): raise Exception(f'Tried to call Node#op() on leaf node!')
    if self.value == '+': return lambda x,y: x+y
    if self.value == '-': return lambda x,y: x-y
    if self.value == '*': return lambda x,y: x*y
    if self.value == '/': return lambda x,y: x//y

  def yell(self):
    if self.is_leaf(): return self.value
    return self.op()(self.left.yell(), self.right.yell())


fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]

# create nodes
nodes_by_name = {}
for line in open(fn, 'r').readlines():
  l = line.strip()
  name, value = l.split(': ')
  nodes_by_name[name] = Node(name, value)

# build nodes into a binary tree structure
for name, node in nodes_by_name.items():
  if not node.is_leaf():
    node.left, node.right = nodes_by_name[node.left], nodes_by_name[node.right]

for k, v in nodes_by_name.items():
  print(k, v)

print(nodes_by_name['root'].yell())
