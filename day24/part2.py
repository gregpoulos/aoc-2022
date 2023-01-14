#!/usr/local/bin/python3

from collections import deque
import sys

WALL  = '#'
LEFT  = '<'
RIGHT = '>'
UP    = '^'
DOWN  = 'v'
DELTAS = {
  UP:    (0, -1),
  DOWN:  (0,  1),
  LEFT:  (-1, 0),
  RIGHT: (1,  0),
}
def tuple_add(t1, t2): return (t1[0]+t2[0], t1[1]+t2[1])
def tuple_subtract(t1, t2): return (t1[0]-t2[0], t1[1]-t2[1])

### VALLEY OBJECT ###

class Valley():
  def __init__(self, grid={}, width=0, height=0):
    self.grid = grid
    self.width = width
    self.height = height

  def __iter__(self):
    self.y = 0
    self.x = 0
    return self
  
  def __next__(self):
    self.x += 1
    if self.x == self.width:
      self.x = 0
      self.y += 1
    if self.y == self.height: 
      raise StopIteration
    return ((self.x, self.y), self.grid[(self.x, self.y)])
 
  def __str__(self):
    def val_to_str(v):
      if type(v) != tuple: return v
      if len(v) == 0: return '.'
      if len(v) == 1: return v[0]
      return str(len(v))
    rows = []
    for y in range(self.height):
      row = []
      for x in range(self.width):
        row.append(val_to_str(self.grid[(x, y)]))
      rows.append(''.join(row))
    return '\n'.join(rows)
 
  def __hash__(self):
    return hash(tuple(val for _, val in self))
 
  def __eq__(self, other):
    return hash(self) == hash(other)
 
  def entrance():
    return (1, 0)
 
  def exit(self):
    return (self.width-2, self.height-1)
 
  def copy(self):
    return Valley(self.grid.copy(), self.width, self.height)
 
  def is_blocked(self, xy):
    return not self.is_open(xy)

  def is_open(self, xy):
    return xy in self.grid and self.grid[xy] == ()
 
  def is_wall(self, xy):
    if xy == Valley.entrance() or xy == self.exit():
      return False
    return xy[0] <= 0 or xy[1] <= 0 or xy[0] >= self.width-1 or xy[1] >= self.height-1

  def add_from_char(self, x, y, val):
    self.width = max(self.width, x+1)
    self.height = max(self.height, y+1)
    if val == '.': val = ()
    if val in {UP, DOWN, LEFT, RIGHT}: val = (val,)
    self.grid[(x, y)] = val
 
  def print_with_expedition(self, exp):
    copy = self.copy()
    copy.grid[exp] = 'E'
    print(copy)

  def neighbors(self, xy):
    return list(map(lambda delta: tuple_add(xy, delta), DELTAS.values()))

  def one_step_away(self, xy):
    candidates = self.neighbors(xy) + [xy]
    return [c for c in candidates if self.is_open(c)]

  def open_spots(self):
    return { xy for xy, _ in self if self.is_open(xy) }
    
  def advance_blizzards(self):
    to_move = []
    for xy, blizzards in self.grid.items():
      if type(blizzards) == tuple:
        for facing in blizzards:
          to_move.append((xy, facing))
    self.delete_blizzards(to_move)
    self.add_blizzards(self.get_new_locations(to_move))

  def add_blizzards(self, blizzards):
    for xy, facing in blizzards:
      self.grid[xy] = tuple(sorted(self.grid[xy] + (facing,)))

  def delete_blizzards(self, blizzards):
    for xy, facing in blizzards:
      here = self.grid[xy]
      if facing in here:
        idx = here.index(facing)
        self.grid[xy] = here[0:idx] + here[idx+1:]

  def get_new_locations(self, blizzards):
    new_locations = []
    for xy, facing in blizzards:
      new_xy = tuple_add(xy, DELTAS[facing])
      if self.is_wall(new_xy):
        new_xy = self.wraparound(xy, facing)
      new_locations.append((new_xy, facing))
    return new_locations

  def wraparound(self, xy, facing):
    next_step = xy
    while not self.is_wall(next_step):
      xy = next_step
      next_step = tuple_subtract(xy, DELTAS[facing])
    return xy

### LIBRARY OBJECT ###

class Library():
  def __init__(self, valley, quiet=True):
    valley = valley.copy() # avoid side effects
    states, minute = {}, 0
    if not quiet: print(f'Building library of possible valley states ...', end='')
    while valley not in states:
      states[valley.copy()] = minute
      minute += 1
      if not quiet and minute % 5 == 0: print('.', end=''); sys.stdout.flush()
      valley.advance_blizzards()
    if not quiet: print(f' done!')
    self.states = [{ v:k for k,v in states.items() }[i] for i in range(len(states))]

  def __len__(self):
    return len(self.states)

  def mod(self, t):
    return t % len(self)

  def at_minute(self, t):
    return (self.states[self.mod(t)], self.mod(t))


### MAIN PROGRAM ###

fn = 'test.txt'
quiet = True
if len(sys.argv) > 1:
  fn = sys.argv[1]
  quiet = False

def parse(fn):
  valley = Valley()
  for y, row in enumerate(open(fn, 'r').readlines()):
    for x, val in enumerate(row.strip()):
      valley.add_from_char(x, y, val)
  return valley

def get_shortest_path_lengths(all_states, destination):
  path_lengths, backlog = {}, deque()
  for t in range(len(all_states)):
    valley, _id = all_states.at_minute(t)
    if valley.is_open(destination):
      path_lengths[(destination, _id)] = 0
      backlog.append((destination, _id))

  while any(backlog):
    exp, _id = backlog.popleft()
    prev_valley, prev_id = all_states.at_minute(_id-1)
    for prev_exp in prev_valley.one_step_away(exp):
      if (prev_exp, prev_id) in path_lengths: continue
      path_lengths[(prev_exp, prev_id)] = path_lengths[(exp, _id)] + 1
      backlog.append((prev_exp, prev_id))
  
  return path_lengths

valley     = parse(fn)
all_states = Library(valley, quiet)
entrance   = Valley.entrance()
exit       = valley.exit()

times_to_exit     = get_shortest_path_lengths(all_states, exit)
times_to_entrance = get_shortest_path_lengths(all_states, entrance)

t = 0
t += times_to_exit[(entrance, all_states.mod(t))]
t += times_to_entrance[(exit, all_states.mod(t))]
t += times_to_exit[(entrance, all_states.mod(t))]
print(t)
