#!/usr/local/bin/python3

class Grid(object):
  def __init__(self):
    self.filled_slots = set()
    self.depth = 0
    self.floor = 0

  def __str__(self):
    xs = [slot[0] for slot in self.filled_slots]
    rows = []
    for j in range(0, self.depth+1):
      row = []
      for i in range(min(xs), max(xs)+1):
        row.append('#' if (i, j) in self.filled_slots else '.')
      rows.append(''.join(row))
    return '\n'.join(rows)

  def set_floor(self):
    self.floor = self.depth + 2

  def add_path(self, path):
    tuples = [list(map(int, t.split(','))) for t in path.split(' -> ')]
    for i in range(0, len(tuples)-1):
      self.add_range(tuples[i], tuples[i+1])

  def add_range(self, start, end):
    if start[0] == end[0]:
      for i in Grid.proper_range(start[1], end[1]): self.fill(start[0], i)
    elif start[1] == end[1]:
      for i in Grid.proper_range(start[0], end[0]): self.fill(i, start[1])

  def proper_range(i, j):
    return range(i, j+1) if i < j else range(j, i+1)

  def is_clear(self, i, j):
    if self.floor and j >= self.floor: return False
    return not (i, j) in self.filled_slots

  def fill(self, i, j):
    if j > self.depth: self.depth = j
    self.filled_slots.add((i, j))

    
# construct grid
g = Grid()
for line in open('input.txt', 'r').readlines():
  g.add_path(line.strip())
g.set_floor()
print(g)

def drop_sand(grid, i, j):
  if grid.is_clear(i, j+1):   return drop_sand(grid, i, j+1)
  if grid.is_clear(i-1, j+1): return drop_sand(grid, i-1, j+1)
  if grid.is_clear(i+1, j+1): return drop_sand(grid, i+1, j+1)
  # base case: sand can't move
  grid.fill(i, j)
  return (i, j)

count = 0
while drop_sand(g, 500, 0) != (500, 0):
  count += 1
print(count+1)
