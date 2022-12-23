#!/usr/local/bin/python3

import networkx as nx
import re
import random

g = nx.Graph()
for line in open('input.txt', 'r').readlines():
  valve, *neighbors = re.findall(r"[A-Z][A-Z]", line)
  g.add_node(valve, flow=int(re.search(r"[0-9]+", line).group()))
  g.add_edges_from([(valve, n) for n in neighbors], weight=1)


def find_next_paths(g):
  me, elephant = g.graph['me'], g.graph['elephant']
  time = g.graph['time']

  my_options = []
  for n, path in nx.single_source_shortest_path(g, me).items():
    if n in g.graph['visited']: continue
    value = (time - len(path)) * g.nodes[n]['flow']
    my_options.append((value, path))

  my_next_path = [me]
  if len(my_options) > 0:
    my_candidates = sorted(my_options, key=lambda x: -x[0])[0:2]  # score
    # my_candidates = sorted(my_options, key=lambda x: len(x[1]))[0:2]  # shortest
    my_next_path = random.sample(my_candidates, 1)[0][1]

  ele_options = []
  for n, path in nx.single_source_shortest_path(g, elephant).items():
    if n in g.graph['visited'] or n == my_next_path[-1]:
      continue
    value = (time - len(path)) * g.nodes[n]['flow']
    ele_options.append((value, path))

  ele_next_path = [elephant]
  if len(ele_options) > 0:
    ele_candidates = sorted(ele_options, key=lambda x: -x[0])[0:2]  # score
    # ele_candidates = sorted(ele_options, key=lambda x: len(x[1]))[0:2]  # shortest
    ele_next_path = random.sample(ele_candidates, 1)[0][1]

  return (my_next_path[1:], ele_next_path[1:])

def maximum_pressure(g):
  score = 0
  time = g.graph['time']
  
  # ignore broken valves by pretending we have already visited them
  if 'visited' not in g.graph: 
    g.graph['visited'] = { n for n in g.nodes if (g.nodes[n]['flow']) == 0 }

  my_route, ele_route = find_next_paths(g)
  
  while time > 0:  
    # print(f'I am in room {g.graph["me"]}')
    # print(f'The elephant is in room {g.graph["elephant"]}')
    # find next best destinations for me and elephant
    if my_route == [] or ele_route == []:
      my_route, ele_route = find_next_paths(g)

    # advance clock by one minute
    time -= 1
    for n in g.graph['visited']:
      if g.nodes[n]['flow'] > 0:
        # print(f'Value {n} is open, producing a flow of {g.nodes[n]["flow"]}')
        score += g.nodes[n]['flow']

    me, elephant = g.graph['me'], g.graph['elephant']
    if my_route == [] and not me in g.graph['visited']:
      # print(f'ACTION] I am opening the valve at {me}')
      g.graph['visited'].add(me)
    elif len(my_route) > 0:
      # print(f'ACTION] I am moving to {my_route[0]}')
      g.graph['me'] = my_route.pop(0)
    
    if ele_route == [] and not elephant in g.graph['visited']:
      # print(f'ACTION] The elephant is opening the valve at {elephant}')
      g.graph['visited'].add(elephant)
    elif len(ele_route) > 0: 
      # print(f'ACTION] The elephant is moving to {ele_route[0]}')
      g.graph['elephant'] = ele_route.pop(0)

    # print(f'---')
  return score

g.graph['me'] = 'AA'
g.graph['elephant'] = 'AA'
g.graph['time'] = 26
results = []
counter = 0
while True:
  counter += 1
  results.append(maximum_pressure(nx.Graph(g)))
  # print(f''); break
  if counter % 5000 == 0:
    best = max(results)
    print(best)
    results = [best]
