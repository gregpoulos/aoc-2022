#!/usr/local/bin/python3

import sys

fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]

drop = set()
area = 0
for line in open(fn, 'r').readlines():
  to_add = 6
  point = tuple([int(i) for i in line.strip().split(',')])
  if (point[0]+1, point[1], point[2]) in drop:
    area -= 1
    to_add -= 1
  if (point[0]-1, point[1], point[2]) in drop:
    area -= 1
    to_add -= 1
  if (point[0], point[1]+1, point[2]) in drop:
    area -= 1
    to_add -= 1
  if (point[0], point[1]-1, point[2]) in drop:
    area -= 1
    to_add -= 1
  if (point[0], point[1], point[2]+1) in drop:
    area -= 1
    to_add -= 1
  if (point[0], point[1], point[2]-1) in drop:
    area -= 1
    to_add -= 1
  drop.add(point)
  area += to_add
print(area)
