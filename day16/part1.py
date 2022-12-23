#!/usr/local/bin/python3

import networkx as nx
import re

g = nx.Graph()
for line in open('input.txt', 'r').readlines():
  valve, *neighbors = re.findall(r"[A-Z][A-Z]", line)
  g.add_node(valve, flow=int(re.search(r"[0-9]+", line).group()))
  g.add_edges_from([(valve, n) for n in neighbors], weight=1)

def best_pressure_release(g, here='AA', time_remaining=30):
  score = 0
  while time_remaining > 0:  
    paths = nx.single_source_shortest_path(g, here)

    # find destination with best payoff
    options = []
    for destination, path in paths.items():
      options.append({
        'destination': destination,
        'path': path,
        'time_cost': len(path),
        'value': (time_remaining - len(path)) * g.nodes[destination]["flow"], 
      })

    if not any(options): break
    if not max([o['value'] for o in options]) > 0: break
    
    # limit recursive calls to best three candidates
    options = sorted(options, key=lambda x: -1*x['value'])
    true_values = []
    for option in options[0:2]:
      true_value = best_pressure_release(
        nx.Graph(g),
        option['destination'],
        time_remaining - option['time_cost'],
      )
      true_values.append(true_value)

    # go to best payoff and update state of world
    best = options[true_values.index(max(true_values))]
    score += best['value']
    time_remaining = time_remaining - best['time_cost']
    g.nodes[best['destination']]['flow'] = 0
    here = best['destination']
  return score

print(best_pressure_release(g))
