#!/usr/local/bin/python3

class Jungle(object):
  def __init__(self, monkeys):
    self.monkeys = monkeys

    

class Monkey(object):
  def __init__(self, items, op, test):
    self.items = items
    self.op = op
    self.test = test
    self.inspections = 0

  def __str__(self):
    return f'Monkey::{self.items} :: {self.inspections} inspections'

  def inspect(self, x):
    self.inspections += 1
    return self.op(x)

items_t = [
  [79, 98],
  [54, 65, 75, 74],
  [79, 60, 97],
  [74],
]

ops_t = [
  lambda x: x*19,
  lambda x: x+6,
  lambda x: x*x,
  lambda x: x+3,
]

tests_t = [
  lambda x: 2 if (x % 23 == 0) else 3,
  lambda x: 2 if (x % 19 == 0) else 0,
  lambda x: 1 if (x % 13 == 0) else 3,
  lambda x: 0 if (x % 17 == 0) else 1,
]

items = [
  [83, 88, 96, 79, 86, 88, 70],
  [59, 63, 98, 85, 68, 72],
  [90, 79, 97, 52, 90, 94, 71, 70],
  [97, 55, 62],
  [74, 54, 94, 76],
  [58],
  [66, 63],
  [56, 56, 90, 96, 68],
]

ops = [
  lambda x: x*5,
  lambda x: x*11,
  lambda x: x+2,
  lambda x: x+5,
  lambda x: x*x,
  lambda x: x+4,
  lambda x: x+6,
  lambda x: x+7,
]

tests = [
  lambda x: 2 if (x % 11 == 0) else 3,
  lambda x: 4 if (x % 5 == 0) else 0,
  lambda x: 5 if (x % 19 == 0) else 6,
  lambda x: 2 if (x % 13 == 0) else 6,
  lambda x: 0 if (x % 7 == 0) else 3,
  lambda x: 7 if (x % 17 == 0) else 1,
  lambda x: 7 if (x % 2 == 0) else 5,
  lambda x: 4 if (x % 3 == 0) else 1,
]


monkeys = []
for item, op, test in zip(items, ops, tests):
  monkeys.append(Monkey(item, op, test))
j = Jungle(monkeys)

for _ in range(20):
  for m in monkeys:
    for _ in range(len(m.items)):
      item = m.items.pop(0)
      item = m.inspect(item)
      item = item // 3
      monkeys[m.test(item)].items.append(item)

for i, m in zip(range(len(monkeys)), monkeys):
  print(f'{i} -- {m}')

