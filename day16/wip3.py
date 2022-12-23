#!/usr/local/bin/python3

import networkx as nx
import re

g = nx.Graph()
for line in open('input.txt', 'r').readlines():
  valve, *neighbors = re.findall(r"[A-Z][A-Z]", line)
  g.add_node(valve, flow=int(re.search(r"[0-9]+", line).group()), open=False)
  g.add_edges_from([(valve, n) for n in neighbors], weight=1)


memo = {}
def evaluate(g):
  global memo
  result = check_memo(g)
  if type(result) == int:
    print(f'cache hit {result}')
    return result
  turn_score = sum(g.nodes[n]['flow'] for n in g.nodes if g.nodes[n]['open'])
  if g.graph['time'] <= 1:
    return turn_score
  else:
    result = max([evaluate(n) for n in get_neighbors(g)]) + turn_score
  memoize(g, result)
  return result


def get_neighbors(g):
  for step1 in get_neighbor_step(g, 'me'):
    for step2 in get_neighbor_step(g, 'elephant'):
      g_ = nx.Graph(g)
      g_.graph['time'] -= 1
      execute_step(g_, step1)
      execute_step(g_, step2)
      yield g_


def get_neighbor_step(g, agent):
  # neighbor universes where agent moves once
  for n in g.neighbors(g.graph[agent]):
    yield (agent, 'move', n)

  # neighbor universes where agent opens a valve
  n = g.graph[agent]
  if g.nodes[n]['flow'] > 0 and not g.nodes[n]['open']:
    yield (agent, 'open', n)


def execute_step(g, step):
  if step[1] == 'move':
    g.graph[step[0]] = step[2]
  else: # step[1] == 'open'
    g.nodes[step[2]]['open'] = True


def check_memo(g):
  global memo
  key = f'{g.graph["me"]}{g.graph["elephant"]}{g.graph["time"]}'
  if key in memo:
    if memo[key][0] == {n for n in g.nodes if g.nodes[n]['open']}:
      return memo[key][1]
  return False

def memoize(g, value):
  global memo
  key = f'{g.graph["me"]}{g.graph["elephant"]}{g.graph["time"]}'
  if key not in memo:
    memo[key] = ({n for n in g.nodes if g.nodes[n]['open']}, value)


g.graph['me'] = 'AA'
g.graph['elephant'] = 'AA'
g.graph['time'] = 10
# for n in g.nodes:
#   print(f'Node {n} has flow {g.nodes[n]["flow"]}')
print(evaluate(g))
