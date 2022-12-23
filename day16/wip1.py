#!/usr/local/bin/python3

import networkx as nx
import re
import random

g = nx.Graph()
for line in open('input.txt', 'r').readlines():
  valve, *neighbors = re.findall(r"[A-Z][A-Z]", line)
  g.add_node(valve, flow=int(re.search(r"[0-9]+", line).group()))
  g.add_edges_from([(valve, n) for n in neighbors], weight=1)


def find_next_path(g, start, time):
  options = []
  for n, path in nx.single_source_shortest_path(g, start).items():
    if (n in g.graph['visited']) or (n not in g.graph['potential_goals']): 
      continue
    value = (time - len(path)) * g.nodes[n]['flow']
    options.append((value, path))
  if options == []: return [start]
  candidates = sorted(options, key=lambda x: -x[0])[0:4]
  return random.sample(candidates, 1)[0][1]
  # return random.sample(options, 1)[0][1]

def maximum_pressure(g, me='AA', elephant='AA', time=26):
  score = 0
  if 'visited' not in g.graph: g.graph['visited'] = set()
  # set up list of valves we may potentially want to visit
  g.graph['potential_goals'] = {
    n for n in g.nodes
    if (g.nodes[n]['flow']) > 0 and (n not in g.graph['visited'])
  }
  # find the first destination for me and the elephant
  my_route = find_next_path(g, me, time)[1:]
  g.graph['potential_goals'].discard(my_route[-1])
  ele_route = find_next_path(g, elephant, time)[1:]
  g.graph['potential_goals'].discard(ele_route[-1])
  while time > 0:  
    # print(f'I am in room {me}')
    # print(f'The elephant is in room {elephant}')
    # find next best destinations for me and elephant
    if my_route == []:
      my_route = find_next_path(g, me, time)
      g.graph['potential_goals'].discard(my_route[-1])
    if ele_route == []:
      ele_route = find_next_path(g, elephant, time)
      g.graph['potential_goals'].discard(ele_route[-1])

    # advance clock by one minute
    time -= 1
    for n in g.graph['visited']:
      # print(f'Value {n} is open, producing a flow of {g.nodes[n]["flow"]}')
      score += g.nodes[n]['flow']

    if me == my_route[0]:
      g.graph['visited'].add(me)
      # print(f'I am opening the valve at {me}')
    me = my_route.pop(0)

    if elephant == ele_route[0]:
      g.graph['visited'].add(elephant)
      # print(f'The elephant is opening the valve at {elephant}')
    elephant = ele_route.pop(0)

    # print('---')
  return score

results = []
counter = 0
while True:
  counter += 1
  results.append(maximum_pressure(nx.Graph(g)))
  if counter % 5000 == 0:
    best = max(results)
    print(best)
    results = [best]
