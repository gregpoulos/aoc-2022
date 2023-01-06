#!/usr/local/bin/python3

import sys
import re

ORE = 'ore'
CLAY = 'cla'
OBSIDIAN = 'obs'
GEODE = 'geo'
RESOURCE_LIST = [ORE, CLAY, OBSIDIAN, GEODE]
TIME = 24

# parse command line args
fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]


memo = {}

class Resources(object):
  def __init__(self, ore=0, cla=0, obs=0, geo=0, name='RESOURCES'):
    self.ore = ore
    self.cla = cla
    self.obs = obs 
    self.geo = geo
    self.name = name

  def __str__(self):
    return f'[<{self.name}> {ORE}: {self.ore} | {CLAY}: {self.cla} | {OBSIDIAN}: {self.obs} | {GEODE}: {self.geo} ]'

  def __hash__(self):
    return hash((self.ore, self.cla, self.obs, self.geo))

  def copy(self):
    return Resources(self.ore, self.cla, self.obs, self.geo, self.name)

  def get(self, r):
    return self.__getattribute__(r)

  def set(self, r, v):
    self.__setattr__(r, v)

  def combine(self, other, fn):
    result = Resources(name=self.name)
    for r in RESOURCE_LIST:
      result.set(r, fn(self.get(r), other.get(r)))
    return result

  def add(self, other):
    return self.combine(other, lambda x,y: x+y)

  def subtract(self, other):
    return self.combine(other, lambda x,y: x-y)

  def add_resource(self, r, n):
    result = self.copy()
    result.set(r, self.get(r)+n)
    return result


class BoardState(object):
  def __init__(self, bank, robots, time):
    self.bank = bank
    self.robots = robots
    self.time = time

  def __str__(self):
    return f'/ [< T={self.time} >]\n| {str(self.bank)}\n\\ {str(self.robots)}'

  def __hash__(self):
    return hash((self.bank, self.robots, self.time))

  def copy(self):
    return BoardState(self.bank.copy(), self.robots.copy(), self.time)

  def build_robot(self, r, bp):
    return BoardState(
      self.bank.subtract(bp.get_cost(r)), 
      self.robots.add_resource(r, 1), 
      self.time
    )

  def wait(self, t):
    result = self.copy()
    for _ in range(t):
      result.bank = result.bank.add(self.robots)
      result.time += 1
    return result


class Blueprint(object):
  def __init__(self, ore, cla, obs, geo):
    self.ore = Resources(ore=ore)
    self.cla = Resources(ore=cla)
    self.obs = Resources(ore=obs[0], cla=obs[1])
    self.geo = Resources(ore=geo[0], obs=geo[1])

  def __str__(self):
    return f'''
> Orebot: {self.ore.ore} ore
> Clabot: {self.cla.ore} ore
> Obsbot: {self.obs.ore} ore, {self.obs.cla} clay
> Geobot: {self.geo.ore} ore, {self.geo.obs} obsidian'''
  
  def get_cost(self, r):
    return self.__getattribute__(r)

  def priciest(self, resource):
    return max([
      self.get_cost(robot_type).get(resource) 
      for robot_type in RESOURCE_LIST
    ])

  def has_budget(self, state, robot_type):
    if state.bank.ore >= self.get_cost(robot_type).ore:
      if robot_type == OBSIDIAN:
        return state.bank.cla >= self.get_cost(OBSIDIAN).cla
      if robot_type == GEODE:
        return state.bank.obs >= self.get_cost(GEODE).obs
      return True
    return False


  def time_to_robot(self, state, robot_type):
    # Returns timestamp by which we'll have resources sufficient to build a
    # robot of `robot_type` given a bank of `resources` and a `fleet` of
    # robot miners. Return `limit` if it takes longer than `limit` to build
    # the robot(e.g., we don't have enough CLAY to build an OBSIDIAN miner
    # and our fleet lacks a CLAY miner).
    # 
    # Note that the return value only considers how long it will take to reach
    # the necessary resources; it does NOT include the time it takes to
    # actually construct the robot.
    if self.has_budget(state, robot_type): return 0
    mining_times = []
    required_resources = [r for r in RESOURCE_LIST if self.get_cost(robot_type).get(r) > 0]
    for r in required_resources:
      rate = state.robots.get(r)
      if rate == 0:
        mining_times.append(TIME)
        continue
      deficit = self.get_cost(robot_type).get(r) - state.bank.get(r)
      turns = deficit // rate
      if deficit % rate != 0: turns += 1 # round up partial turns
      mining_times.append(turns)
    return max(mining_times)



def memoized(bp, strategy, state, value):
  global memo
  if (bp, tuple(strategy), state) not in memo:
    memo[(bp, tuple(strategy), state)] = value
  return value


def is_feasible(bp, strategy, state):
  global memo
  if (bp, tuple(strategy), state) in memo: return memo[(bp, tuple(strategy), state)]
  # A strategy consists of a list of times at which we will build a
  # geode-mining robot. This function determines whether a strategy can
  # actually be executed.
  if len(strategy) < 1: return True
  result = any([
    is_feasible(bp, strategy[1:], future_state)
    for future_state in get_possible_futures(bp, state, strategy[0])
  ])
  return memoized(bp, strategy, state, result)
  

def get_possible_futures(bp, state, target_time):
  # This function returns all possible future states in which the next
  # GEODE-mining robot is built at minute `target_time`.
  futures = set()
  # will we be able to build a GEODE-mining robot if we just wait?
  if state.time + bp.time_to_robot(state, GEODE) < target_time:
    futures.add(state.wait(target_time - state.time).build_robot(GEODE, bp))

  # next, consider building each other type of robot
  for r in [ORE, CLAY, OBSIDIAN]:
    if bp.priciest(r) <= state.robots.get(r): continue
    wait_time = bp.time_to_robot(state, r)
    if state.time + wait_time < target_time - 1:
      new_state = state.wait(wait_time + 1).build_robot(r, bp)
      futures.update(get_possible_futures(bp, new_state, target_time))
  return futures


def geodes_mined(strategy):
  geodes_mined = 0
  for build_time in strategy:
    geodes_mined += TIME - build_time
  return geodes_mined


def bitmasks(i):
  if i <= 0: yield []
  else:
    for rest in bitmasks(i-1):
      yield [0] + rest
      yield [1] + rest


def compute_earliest_build_time(bp):
  out = 0
  for r in [CLAY, OBSIDIAN, GEODE]:
    n = 0
    while n * (n+1) - bp.get_cost(r).ore * 2 <= 0: n += 1
    out += n
  return out


# read in blueprints
blueprints = []
for line in open(fn, 'r').readlines():
  p = list(map(lambda x: int(x), re.findall(r"[0-9][0-9]?", line)))
  blueprints.append(Blueprint(p[1], p[2], (p[3], p[4]), (p[5], p[6])))

total_quality = 0
for i, bp in enumerate(blueprints):
  strategies = []
  earliest_build_time = 18 #compute_earliest_build_time(bp)
  for bitmask in bitmasks(TIME - earliest_build_time + 1):
    strategies.append([
      idx + earliest_build_time
      for idx, value in enumerate(bitmask) if value == 1
    ])
  strategies = sorted(strategies, key=lambda x: -geodes_mined(x))

  for s in strategies:
    bank = Resources(0, 0, 0, 0, ' BANK ')
    robots = Resources(1, 0, 0, 0, 'ROBOTS')
    state = BoardState(bank, robots, 0)
    if is_feasible(bp, s, state):
      geodes = geodes_mined(s)
      print(f'Blueprint #{i+1}: Best strategy {s} mines {geodes} geodes')
      total_quality += (i+1) * geodes
      break

print(f'Total quality: {total_quality}')

# Blueprint #29: I got 0, answer is 1 
