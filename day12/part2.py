#!/usr/local/bin/python3

class Node(object):
  def __init__(self, height, neighbors=[]):
    self.height = Node.normalize_height(height)
    self.neighbors = set()
    self.distance = None
    self.is_start = (height == 'S')
    self.is_end = (height == 'E')

  def __str__(self):
    return f'NODE({self.height} | # neighbors: {len(self.neighbors)})'

  def add_neighbor(self, neighbor):
    self.neighbors.add(neighbor)

  def is_walkable(self, neighbor):
    return ord(neighbor.height) - ord(self.height) >= -1

  def get_unvisited_neighbors(self):
    return [n for n in self.neighbors if not n.distance]

  def normalize_height(height):
    if height == 'S': return 'a'
    if height == 'E': return 'z'
    return height


def connect_neighbors(grid, i, j):
  def is_on_grid(idx): # check if (i, j) is a point that exists on the grid
    return (0 <= idx[0] and idx[0] < len(grid) and 
            0 <= idx[1] and idx[1] < len(grid[0]))
  for i_n, j_n in filter(is_on_grid, [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]):
    this_node = grid[i][j]
    neighbor = grid[i_n][j_n]
    if this_node.is_walkable(neighbor): this_node.add_neighbor(neighbor)

def mark_distances(nodes, depth=0):
  to_visit_next = set()
  for node in nodes:
    if node.distance == None: node.distance = depth
    to_visit_next.update(node.get_unvisited_neighbors())
  if any(to_visit_next):
    mark_distances(to_visit_next, depth+1)

def print_grid(grid):
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      here = grid[i][j]
      if not here.distance:
        print('.', end='')
      else:
        print(here.height, end='')
    print('\n', end='')


# read input
grid = [
  [Node(c) for c in list(line.strip())]
  for line in open('input.txt', 'r').readlines()
]

# build graph
start = None
end = None
for i in range(len(grid)):
  for j in range(len(grid[0])):
    here = grid[i][j]
    if here.is_start: start = grid[i][j]
    if here.is_end: end = grid[i][j]
    connect_neighbors(grid, i, j)

mark_distances([end])
print_grid(grid)
candidates = set()
for i in range(len(grid)):
  for j in range(len(grid[0])):
    here = grid[i][j]
    if here.height == 'a' and here.distance != None:
      candidates.add(here.distance)
print(min(candidates))
