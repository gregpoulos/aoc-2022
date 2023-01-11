#!/usr/local/bin/python3

import re
import sys

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

class Grid():
  def __init__(self):
    self.grid = {}
    self.width = 0
    self.height = 0
    self.caches = {
      UP: {}, DOWN: {}, LEFT: {}, RIGHT: {}
    }

  def __contains__(self, pt):
    return pt in self.grid

  def __str__(self):
    result = []
    for y in range(1, self.height+1):
      row = []
      for x in range(1, self.width+1):
        row.append(self.grid[(x, y)] if (x, y) in self.grid else ' ')
      result.append(''.join(row))
    return '\n'.join(result)

  def get(self, x, y):
    return self.grid[(x, y)]

  def is_open(self, x, y):
    return (x, y) in self and self.get(x, y) == '.'

  def add(self, x, y, val):
    if (x, y) in self:
      raise Exception("Called Grid#add() with point that already exists!")
    self.grid[(x, y)] = val
    self.width = max(self.width, x)
    self.height = max(self.height, y)

  def next(self, x, y, facing):
    if facing == UP:      x_inc, y_inc = 0 ,-1
    elif facing == DOWN:  x_inc, y_inc = 0 , 1
    elif facing == LEFT:  x_inc, y_inc = -1, 0
    elif facing == RIGHT: x_inc, y_inc = 1 , 0

    if (x+x_inc, y+y_inc) in self.grid: 
      return (x+x_inc, y+y_inc)
    if (x, y) in self.caches[facing]: 
      return self.caches[facing][(x, y)]
    new_x, new_y = x, y
    while (new_x-x_inc, new_y-y_inc) in self.grid: 
      new_x, new_y = new_x-x_inc, new_y-y_inc
    self.caches[facing][(x, y)] = (new_x, new_y)
    return (new_x, new_y)

  def up_1(self, x, y):
    return self.next(x, y, UP)

  def down_1(self, x, y):
    return self.next(x, y, DOWN)

  def left_1(self, x, y):
    return self.next(x, y, LEFT)

  def right_1(self, x, y):
    return self.next(x, y, RIGHT)


class Agent():
  def __init__(self, grid):
    self.grid = grid
    self.facing = RIGHT
    self.y = 1
    self.x = 1
    while not grid.is_open(self.x, 1): self.x+=1

  def pos(self):
    return (self.x, self.y)

  def step(self, n):
    for _ in range(n):
      one_step = self.grid.next(self.x, self.y, self.facing)
      if self.grid.get(*one_step) == '#': break
      self.x, self.y = one_step

  def turn_r(self):
    self.facing = (self.facing + 1) % 4

  def turn_l(self):
    self.facing = (self.facing - 1) % 4

  def get_password(self):
    return 1000 * self.y + 4 * self.x + self.facing


fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]

# construct grid
grid = Grid()
lines = None
with open(fn, 'r') as f:
  lines = f.read().split('\n')
_map, path = lines[:-3], lines[-2]
for y, row in enumerate(_map):
  for x in range(len(row)):
    if row[x] in {'.', '#'}: grid.add(x+1, y+1, row[x])

# extract commands from string
commands = []
for match in re.finditer(r'(\d+)([RL])?', path):
  commands.append(int(match.group(1)))
  if match.group(2): commands.append(match.group(2))

a = Agent(grid)
for command in commands:
  if type(command) == int:
    a.step(command)
  elif command == 'R':
    a.turn_r()
  else: # if command == 'L'
    a.turn_l()

print(a.get_password())
