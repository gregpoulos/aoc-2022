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

  def compute_scenicness(self):
    for i in range(self.depth):
      for j in range(self.width):
        cur_tree = self.trees[i][j]
        def get_score(ts):
          score = 0
          for t in ts:
            score += 1
            if t.height >= cur_tree.height:
              break
          return score
        cur_tree.scenic_score = (
          get_score(reversed(self.north_of(i, j))) *
          get_score(self.south_of(i, j)) *
          get_score(self.east_of(i, j)) *
          get_score(reversed(self.west_of(i, j)))
        )

  def max_scenicness(self):
    return max([
      max([tree.scenic_score for tree in row])
      for row in self.trees
    ])
    

class Tree(object):
  """docstring for Tree"""
  def __init__(self, height, visible = True, scenic_score = 0):
    self.height = int(height)
    self.visible = visible
    self.scenic_score = scenic_score
    
  def __str__(self):
    return str(self.height) if self.visible else 'X'


f = open('input.txt', 'r')
heights = f.read().strip()
fst = Forest(heights)
f.close()
fst.compute_scenicness()
print(fst.max_scenicness())
