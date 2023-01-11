#!/usr/local/bin/python3

import math
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
    self.ijk_to_xy = None
    self.xy_to_ijk = None

  def __contains__(self, pt):
    return pt in self.grid

  def __str__(self):
    return '\n'.join([
      ''.join([
        self.grid[(x, y)] if (x, y) in self.grid else ' '
        for x in range(1, self.width+1)])
      for y in range(1, self.height+1)])

  def init_cube(self):
    # The dicts xy_to_ijk and ijk_to_xy allow us to map from the standard
    # (x, y) grid coordinates to 3-D (i, j, k) coordinates, where i is the
    # cube face ID and (j, k) are the point's position relative to the
    # origin (1, 1) in the upper-left corner of the cube face
    self.ijk_to_xy = {}
    self.xy_to_ijk = {}
    self.N = math.isqrt(self.width * self.height // 12)
    i = 0
    for y_start in range(1, self.height+1, self.N):
      for x_start in range(1, self.width+1, self.N):
        if not (x_start, y_start) in self: continue
        i += 1
        for y in range(y_start, y_start+self.N):
          for x in range(x_start, x_start+self.N):
            assert (x, y) in self
            j, k = x-x_start+1, y-y_start+1
            self.ijk_to_xy[(i, j, k)] = (x, y)
            self.xy_to_ijk[(x, y)] = (i, j, k)

  def get(self, x, y, z=None):
    if z: (x, y) = self.ijk_to_xy[(x, y, z)]
    return self.grid[(x, y)]

  def is_open(self, x, y, z=None):
    if z: (x, y) = self.ijk_to_xy[(x, y, z)]
    return (x, y) in self and self.get(x, y) == '.'

  def add(self, x, y, val):
    if (x, y) in self:
      raise Exception("Called Grid#add() with point that already exists!")
    self.grid[(x, y)] = val
    self.width = max(self.width, x)
    self.height = max(self.height, y)

  def next(self, x, y, facing):
    if   facing == RIGHT: x_inc, y_inc = 1 , 0
    elif facing == DOWN:  x_inc, y_inc = 0 , 1
    elif facing == LEFT:  x_inc, y_inc = -1, 0
    elif facing == UP:    x_inc, y_inc = 0 ,-1
    if (x+x_inc, y+y_inc) in self.grid: 
      return (x+x_inc, y+y_inc), facing
    # if walking off edge of cube, perform rotation operation
    return self.next_with_rotate(x, y, facing)
    
  def next_with_rotate(self, _x, _y, facing):
    if not self.xy_to_ijk: self.init_cube()
    face_id, x, y = self.xy_to_ijk[(_x, _y)]

    if facing == RIGHT: assert x == self.N
    if facing == DOWN:  assert y == self.N
    if facing == LEFT:  assert x == 1
    if facing == UP:    assert y == 1

    i,j,k,f = (None, None, None, None)
    # rotation operation for input.txt
    if face_id == 1:
      if facing == RIGHT: i,j,k,f = (2, 1, y, RIGHT)
      if facing == DOWN:  i,j,k,f = (3, x, 1, DOWN)
      if facing == LEFT:  i,j,k,f = (4, 1, self.N-y+1, RIGHT)
      if facing == UP:    i,j,k,f = (6, 1, x, RIGHT)
    if face_id == 2:
      if facing == RIGHT: i,j,k,f = (5, self.N, self.N-y+1, LEFT)
      if facing == DOWN:  i,j,k,f = (3, self.N, x, LEFT)
      if facing == LEFT:  i,j,k,f = (1, self.N, y, LEFT)
      if facing == UP:    i,j,k,f = (6, x, self.N, UP)
    if face_id == 3:
      if facing == RIGHT: i,j,k,f = (2, y, self.N, UP)
      if facing == DOWN:  i,j,k,f = (5, x, 1, DOWN)
      if facing == LEFT:  i,j,k,f = (4, y, 1, DOWN)
      if facing == UP:    i,j,k,f = (1, x, self.N, UP)
    if face_id == 4:
      if facing == RIGHT: i,j,k,f = (5, 1, y, RIGHT)
      if facing == DOWN:  i,j,k,f = (6, x, 1, DOWN)
      if facing == LEFT:  i,j,k,f = (1, 1, self.N-y+1, RIGHT)
      if facing == UP:    i,j,k,f = (3, 1, x, RIGHT)
    if face_id == 5:
      if facing == RIGHT: i,j,k,f = (2, self.N, self.N-y+1, LEFT)
      if facing == DOWN:  i,j,k,f = (6, self.N, x, LEFT)
      if facing == LEFT:  i,j,k,f = (4, self.N, y, LEFT)
      if facing == UP:    i,j,k,f = (3, x, self.N, UP)
    if face_id == 6:
      if facing == RIGHT: i,j,k,f = (5, y, self.N, UP)
      if facing == DOWN:  i,j,k,f = (2, x, 1, DOWN)
      if facing == LEFT:  i,j,k,f = (1, y, 1, DOWN)
      if facing == UP:    i,j,k,f = (4, x, self.N, UP)

    # # rotation operation for test.txt
    # if face_id == 1:
    #   if facing == RIGHT: i,j,k,f = (6, self.N, self.N-y+1, LEFT)
    #   if facing == DOWN:  i,j,k,f = (4, x, 1, DOWN)
    #   if facing == LEFT:  i,j,k,f = (3, y, 1, DOWN)
    #   if facing == UP:    i,j,k,f = (2, self.N-x+1, 1, DOWN)
    # if face_id == 2:
    #   if facing == RIGHT: i,j,k,f = (3, 1, y, RIGHT)
    #   if facing == DOWN:  i,j,k,f = (5, self.N-x+1, self.N, UP)
    #   if facing == LEFT:  i,j,k,f = (6, self.N-y+1, self.N, UP)
    #   if facing == UP:    i,j,k,f = (1, self.N-x+1, 1, DOWN)
    # if face_id == 3:
    #   if facing == RIGHT: i,j,k,f = (4, 1, y, RIGHT)
    #   if facing == DOWN:  i,j,k,f = (5, 1, self.N-x+1, RIGHT)
    #   if facing == LEFT:  i,j,k,f = (2, self.N, y, LEFT)
    #   if facing == UP:    i,j,k,f = (1, 1, x, RIGHT)
    # if face_id == 4:
    #   if facing == RIGHT: i,j,k,f = (6, self.N-y+1, 1, DOWN)
    #   if facing == DOWN:  i,j,k,f = (5, x, 1, DOWN)
    #   if facing == LEFT:  i,j,k,f = (3, self.N, y, LEFT)
    #   if facing == UP:    i,j,k,f = (1, x, self.N, UP)
    # if face_id == 5:
    #   if facing == RIGHT: i,j,k,f = (6, 1, y, RIGHT)
    #   if facing == DOWN:  i,j,k,f = (2, self.N-x+1, self.N, UP)
    #   if facing == LEFT:  i,j,k,f = (3, self.N-y+1, self.N, UP)
    #   if facing == UP:    i,j,k,f = (4, x, self.N, UP)
    # if face_id == 6:
    #   if facing == RIGHT: i,j,k,f = (1, self.N, self.N-y+1, LEFT)
    #   if facing == DOWN:  i,j,k,f = (2, 1, self.N-x+1, RIGHT)
    #   if facing == LEFT:  i,j,k,f = (5, self.N, y, LEFT)
    #   if facing == UP:    i,j,k,f = (4, self.N, self.N-x+1, LEFT)

    return self.ijk_to_xy[(i, j, k)], f


class Agent():
  def __init__(self, grid):
    self.grid = grid
    self.facing = RIGHT
    self.y = 1
    self.x = 1
    while not grid.is_open(self.x, 1): self.x+=1

  def step(self, n):
    for _ in range(n):
      (new_x, new_y), new_facing = self.grid.next(self.x, self.y, self.facing)
      if self.grid.get(new_x, new_y) == '#': break
      self.x, self.y, self.facing = new_x, new_y, new_facing

  def turn_r(self):
    self.facing = (self.facing + 1) % 4

  def turn_l(self):
    self.facing = (self.facing - 1) % 4

  def get_password(self):
    return 1000 * self.y + 4 * self.x + self.facing

    
def parse_input(fn):
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

  return grid, commands


fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]

grid, commands = parse_input(fn)
a = Agent(grid)
for command in commands:
  if type(command) == int:
    a.step(command)
  elif command == 'R':
    a.turn_r()
  else: # if command == 'L'
    a.turn_l()

print(a.get_password())
