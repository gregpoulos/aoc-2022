#!/usr/local/bin/python3

import sys

LAVA = -1
SIZE = 7
fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]
  SIZE = 20


class Drop(object):
  def __init__(self, size):
    self.size = size
    self.points = [[[None for _ in range(size)] for _ in range(size)] for _ in range(size)]
    self.area = 0

  def add_point(self, x, y, z):
    if self.points[x][y][z] == LAVA:
      return
    to_add = 6
    for i,j,k in self.get_neighbors(x, y, z):
      if self.points[i][j][k] == LAVA:
        self.area -= 1
        to_add -= 1
    self.points[x][y][z] = LAVA
    self.area += to_add

  def get_neighbors(self, x, y, z):
    ret = []
    if x+1 < self.size: ret.append((x+1,y,z))
    if y+1 < self.size: ret.append((x,y+1,z))
    if z+1 < self.size: ret.append((x,y,z+1))
    if x-1 >= 0: ret.append((x-1,y,z))
    if y-1 >= 0: ret.append((x,y-1,z))
    if z-1 >= 0: ret.append((x,y,z-1))
    return ret

  def color(self, x, y, z, val):
    if self.points[x][y][z]: return
    to_color = {(x,y,z)}
    while any(to_color):
      i,j,k = to_color.pop()
      self.points[i][j][k] = val
      for a,b,c in self.get_neighbors(i,j,k):
        if not self.points[a][b][c]:
          to_color.add((a,b,c))
  

d = Drop(SIZE)
for line in open(fn, 'r').readlines():
  point = tuple([int(i) for i in line.strip().split(',')])
  d.add_point(*point)

i = 0
for x in range(SIZE):
  for y in range(SIZE):
    for z in range(SIZE):
      i += 1
      d.color(x, y, z, i)

for x in range(SIZE):
  for y in range(SIZE):
    for z in range(SIZE):
      if d.points[x][y][z] > 1:
        d.add_point(x, y, z)

print(d.area)
