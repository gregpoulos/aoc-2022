#!/usr/local/bin/python3

import math
import sys

NORTH = (0, -1)
SOUTH = (0, 1)
EAST  = (1, 0)
WEST  = (-1, 0)
NW    = (-1, -1)
SW    = (-1, 1)
NE    = (1, -1)
SE    = (1, 1)
DIRECTIONS = [NORTH, SOUTH, EAST, WEST, NW, SW, NE, SE]
CHECKLIST = {
  NORTH: [NW, NORTH, NE],
  SOUTH: [SW, SOUTH, SE],
  WEST:  [NW, WEST,  SW],
  EAST:  [NE, EAST,  SE],
}

def plus(x, y):
  return (x[0]+y[0], x[1]+y[1])

fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]

class Grid():
  def __init__(self):
    self.elves = set()
    self.x_min, self.y_min = math.inf, math.inf
    self.x_max, self.y_max = -math.inf, -math.inf
    self.cycle = [NORTH, SOUTH, WEST, EAST]

  def __contains__(self, elf):
    return elf in self.elves

  def __str__(self):
    if any(math.isinf(x) for x in [self.x_min, self.y_min, self.x_max, self.y_max]): return ''
    return '\n'.join([
      ''.join([
        '#' if (x, y) in self.elves else '.'
        for x in range(self.x_min, self.x_max+1)
      ]) for y in range(self.y_min, self.y_max+1)])

  def count_empty(self):
    count = 0
    x_min = min(elf[0] for elf in self.elves)
    x_max = max(elf[0] for elf in self.elves)
    y_min = min(elf[1] for elf in self.elves)
    y_max = max(elf[1] for elf in self.elves)
    for y in range(y_min, y_max+1):
      for x in range(x_min, x_max+1):
        if (x, y) not in self:
          count += 1
    return count

  def add_elf(self, x, y):
    self.elves.add((x, y))
    self.x_min = min(x, self.x_min)
    self.y_min = min(y, self.y_min)
    self.x_max = max(x, self.x_max)
    self.y_max = max(y, self.y_max)

  def move_elf(self, elf, destination):
    self.elves.remove(elf)
    self.add_elf(*destination)

  def advance_cycle(self):
    self.cycle.append(self.cycle.pop(0))

  def get_proposals(self):
    # Returns `proposals`, a dict where each key is a proposed destination and
    # each value is a list of elves that want to move to that destination.
    # Ideally, each destination only has one elf that wants to go there.
    proposals = {}
    for elf in self.elves:
      dest = self.get_proposal(elf)
      if not dest: continue
      if dest in proposals:
        proposals[dest].append(elf)
      else:
        proposals[dest] = [elf]
    return proposals

  def get_proposal(self, elf):
    # Returns a proposed destination for this elf, based on the current
    # check-cycle. Returns None if the elf won't move, either because it has
    # no neighbors or because it sees a neighbor in every direction.
    if not any(plus(elf, d) in self.elves for d in DIRECTIONS):
      return None
    for direction in self.cycle:
      if all(plus(elf, delta) not in self.elves for delta in CHECKLIST[direction]):
        return plus(elf, direction) # no neighbor elf in this direction
    return None


grid = Grid()
for row, line in enumerate(open(fn, 'r').readlines()):
  for col, char in enumerate(line.strip()):
    if char == '#': grid.add_elf(col, row)

for _ in range(10):
  proposals = grid.get_proposals()
  for destination, elves in proposals.items():
    if len(elves) == 1:
      grid.move_elf(elves[0], destination)
  grid.advance_cycle()

print(grid.count_empty())
