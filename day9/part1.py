#!/usr/local/bin/python3
from collections import defaultdict

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def move(self, direction):
    if len(direction) > 1:
      for d in list(direction):
        Point.move(self, d)
    if direction == 'U':
      self.y += 1
    elif direction == 'D':
      self.y -= 1
    elif direction == 'L':
      self.x -= 1
    elif direction == 'R':
      self.x += 1

  def __str__(self):
    return 'f({x}, {y})'

    
class Tail(Point):
  def move(self, direction, board):
    super().move(direction)
    board.visit(self.x, self.y)


class Board(object):
  """docstring for Board"""
  def __init__(self):
    self.board = defaultdict(dict)

  def size(self):
    min_x, max_x, min_y, max_y = 0, 0, 0, 0
    if any(self.board.keys()):
      min_y = min(self.board.keys())
      max_y = max(self.board.keys())
    for k, v in self.board.items():
      if any(v):
        min_x = min(min_x, min(v.keys()))
        max_x = max(max_x, max(v.keys()))
    return (min_x, max_x, min_y, max_y)

  def visit(self, x, y):
    self.board[y][x] = True

  def visited(self, x, y):
    return self.board[y].get(x)

  def count_visited(self):
    total = 0
    for _, v in self.board.items():
      total += len(v)
    return total

  def __str__(self):
    min_x, max_x, min_y, max_y = self.size()
    rows = []
    for y in range(min_y, max_y+1):
      row = []
      for x in range(min_x, max_x+1):
        row.append('#' if self.visited(x, y) else '.')
      rows.append(' '.join(row))
    return '\n'.join(reversed(rows))



def compute_move(head, tail):
  if abs(head.x - tail.x) <= 1 and abs(head.y - tail.y) <= 1:
    print('tail does not move')
    return ''
  dirs = []
  if head.x == tail.x:
    dirs.append('U' if (head.y > tail.y) else 'D')
  elif head.y == tail.y:
    dirs.append('R' if (head.x > tail.x) else 'L')
  else:
    dirs.append('R' if (head.x > tail.x) else 'L')
    dirs.append('U' if (head.y > tail.y) else 'D')
  print(f'computed tail move: {"".join(dirs)}')
  return ''.join(dirs)



def debug_print(board, head, tail):
  min_x, max_x, min_y, max_y = board.size()
  min_x = min(min_x, head.x, tail.x)
  min_y = min(min_y, head.y, tail.y)
  max_x = max(max_x, head.x, tail.x)
  max_y = max(max_y, head.y, tail.y)
  print(f'board size: {min_x}<-->{max_x} x {min_y}<-->{max_y}')
  print(f'board size: {abs(max_x) + abs(min_x) + 1} x {abs(max_y) + abs(min_y) + 1}')
  print(f'head: ({head.x}, {head.y}) | tail: ({tail.x}, {tail.y})')
  rows = []
  for y in range(min_y, max_y+1):
    row = []
    for x in range(min_x, max_x+1):
      if x == head.x and y == head.y:
        row.append('H')
      elif x == tail.x and y == tail.y:
        row.append('T')
      else:
        row.append('.')
    rows.append(''.join(row))
  print('\n'.join(reversed(rows)))



counter = 0
head = Point(0, 0)
tail = Tail(0, 0)
board = Board()

for line in open('input.txt', 'r').readlines():
  # counter += 1
  # if counter > 100:
  #   break
  direction, times = line.strip().split(' ')
  print(f'### READING COMMAND {direction} {times} ###')
  for i in range(int(times)):
    print(f'moving head {direction}')
    head.move(direction)
    tail.move(compute_move(head, tail), board)
    # debug_print(board, head, tail)
    print('--------------')

print(board)
print(f'The tail visited {board.count_visited()} unique spots on the board.')
