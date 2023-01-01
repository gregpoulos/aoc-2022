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
    self.height = 0 if not any(self.points) else max({y for _, y in self.points}) + 1

  def add(self, rock):
    self.height = max(self.height, rock.height)
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
    self.height -= 1
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

  def get_skyline(self):
    skyline = []
    for i in range(7):
      column = {y for (x, y) in self.points if x == i}
      skyline.append(0 if not column else max(column)+1)
    return tuple([val - min(skyline) for val in skyline])

  def __str__(self):
    rows = []
    for y in range(self.height):
      rows.append(''.join([
        '#' if (x, y) in self.points else '.'
        for x in range(7)
      ]))
    rows.insert(0, '\n')
    return '\n'.join(reversed(rows))


pile = Rock(None)
shape_counter, blast_counter = 0, 0
this_rock = Rock(pile, shape=SHAPES[shape_counter], height=3)
cycle = len(SHAPES) * len(BLASTS)
seen_states = {
  ((0, 0, 0, 0, 0, 0, 0), 0, 0): 0
}

# MAIN LOOP #
while True:
  # blast rock left or right
  this_rock.push_1(BLASTS[blast_counter%len(BLASTS)])
  blast_counter += 1

  # can I fall one unit down?
  if this_rock.can_fall():
    this_rock.fall_1()
    continue

  # add fallen rock to the pile
  pile.add(this_rock)
  shape_counter += 1

  # register the current state
  this_state = (
    pile.get_skyline(), 
    shape_counter%len(SHAPES),
    blast_counter%len(BLASTS),
  )
  if this_state in seen_states:
    print(f'state {seen_states[this_state]} is repeated ... quitting')
    break
  else:
    seen_states[this_state] = shape_counter

  # # terminate after dropping X rocks
  # if shape_counter >= 1600:
  #   break

  # spawn a new rock
  this_rock = Rock(pile, shape=SHAPES[shape_counter%len(SHAPES)], height=pile.height+3)


print(f'{shape_counter} rocks have fallen')
print(f'pile is {pile.height} units tall')


# cycle begins repeating itself at rock 980
# first repeated state is rock 2705
# cycle has length of 2705 - 980 = 1725
# height of pile at 980 = 1521 units
# height of pile at 2705 = 4249 units
# each cycle adds 4249 - 1521 = 2728 units
# 1000000000000 = 980 + 1725 * #cycles + remainder
# #cycles = 579710144
# remainder = 620 rocks
# height of head = 1521
# height of body of cycles = 579710144 * 2728 = 1581449272832
# height of remainder = [height at rock 980+620] - [height at rock 980]
#                     = 2487 - 1521 = 966
# total height = 1521 + 1581449272832 + 966
