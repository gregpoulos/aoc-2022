#!/usr/local/bin/python3

class Forest(object):
  """docstring for Forest"""
  def __init__(self, heights):
    self.trees = []
    for row in heights.split('\n'):
      self.trees.append([Tree(h) for h in list(row)])
    self.depth = len(self.trees)
    self.width = len(self.trees)

  def __str__(self):
    return '\n'.join([', '.join(map(str, row)) for row in self.trees])

  def get_tree(self, i, j):
    return self.trees[i][j]

  def north_of(self, i, j):
    col = []
    for row in self.trees[:i]:
      col.append(row[j])
    return col

  def south_of(self, i, j):
    col = []
    for row in self.trees[i+1:]:
      col.append(row[j])
    return col

  def east_of(self, i, j):
    return self.trees[i][j+1:]

  def west_of(self, i, j):
    return self.trees[i][0:j]

  def compute_visibilities(self):
    for i in range(self.depth):
      for j in range(self.width):
        cur_tree = self.trees[i][j]
        cur_height = cur_tree.height
        if (
          any(t.height >= cur_height for t in self.north_of(i, j)) and
          any(t.height >= cur_height for t in self.south_of(i, j)) and
          any(t.height >= cur_height for t in self.east_of(i, j)) and
          any(t.height >= cur_height for t in self.west_of(i, j))
        ):
           cur_tree.visible = False

  def count_visible(self):
    return sum([
      sum([(1 if t.visible else 0) for t in row])
      for row in self.trees
    ])


class Tree(object):
  """docstring for Tree"""
  def __init__(self, height, visible = True):
    self.height = int(height)
    self.visible = visible
    
  def __str__(self):
    return str(self.height) if self.visible else 'X'


f = open('input.txt', 'r')
heights = f.read().strip()
fst = Forest(heights)
f.close()

fst.compute_visibilities()
print(fst.count_visible())
