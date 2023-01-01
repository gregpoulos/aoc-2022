#!/usr/local/bin/python3

import sys

fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]

SHAPES = ['-', '+', 'L', 'I', 'O']
BLASTS = []
for b in open(fn, 'r').read():
  if b in {'<', '>'}:
    BLASTS.append(b)

class Rock(object):
  def __init__(self, pile, shape=None, height=0):
    self.pile = pile
    if shape == '-':
      self.points = {(2, height), (3, height), (4, height), (5, height),}
    elif shape == '+':
      self.points = {(2, height+1), (3, height), (3, height+1), (3, height+2), (4, height+1),}
    elif shape == 'L':
      self.points = {(2, height), (3, height), (4, height), (4, height+1), (4, height+2),}
    elif shape == 'I':
      self.points = {(2, height), (2, height+1), (2, height+2), (2, height+3),}
    elif shape == 'O':
      self.points = {(2, height), (2, height+1), (3, height), (3, height+1),}
    else:
      self.points = set()

  def add(self, rock):
    self.points.update(rock.points)

  def push_1(self, direction):
    if direction == '<':
      if not self.collide_left(self.pile):
        self.push_1(-1)
    elif direction == '>':
      if not self.collide_right(self.pile):
        self.push_1(1)
    else:
      self.points = {(x+direction, y) for (x, y) in self.points}

  def fall_1(self):
    self.points = {(x, y-1) for (x, y) in self.points}

  def can_fall(self):
    return not self.collide_down(self.pile)

  def collide_right(self, other):
    return any({
      x+1 >= 7 or (x+1, y) in other.points 
      for x, y in self.points
    })

  def collide_left(self, other):
    return any({
      x-1 < 0 or (x-1, y) in other.points 
      for x, y in self.points
    })

  def collide_down(self, other):
    return any({
      y-1 < 0 or (x, y-1) in other.points 
      for x, y in self.points
    })

  def height(self):
    return 0 if not any(self.points) else max({y for _, y in self.points})+1

  def __str__(self):
    rows = []
    for y in range(self.height()):
      rows.append(''.join([
        '#' if (x, y) in self.points else '.'
        for x in range(7)
      ]))
    rows.insert(0, '\n')
    return '\n'.join(reversed(rows))


pile = Rock(None)
shape_counter, blast_counter = 0, 0

this_rock = Rock(pile, shape=SHAPES[shape_counter], height=3)
shape_counter += 1

while True:
  # blast rock left or right
  this_rock.push_1(BLASTS[blast_counter%len(BLASTS)])
  blast_counter += 1

  # can I fall one unit down?
  if this_rock.can_fall():
    this_rock.fall_1()
  else:
    pile.add(this_rock)
    this_rock = Rock(pile, shape=SHAPES[shape_counter%5], height=pile.height()+3)
    shape_counter += 1
  if shape_counter == 2023:
    break

print(pile.height())
