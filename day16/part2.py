#!/usr/local/bin/python3

import networkx as nx
import re
import itertools
import sys

# read in graph from input
g = nx.Graph()
g.graph['to_visit'] = []
for line in open('input.txt', 'r').readlines():
  valve, *neighbors = re.findall(r"[A-Z][A-Z]", line)
  flow = int(re.search(r"[0-9]+", line).group())
  if flow > 0:
    g.graph['to_visit'].append(valve)
  g.add_node(valve, flow=flow)
  g.add_edges_from([(valve, n) for n in neighbors])

# memoize shortest paths between each pair of nodes in graph
all_shortest_paths = {}
for source, dests in nx.all_pairs_shortest_path(g):
  all_shortest_paths[source] = {}
  for dest, path in dests.items():
    all_shortest_paths[source][dest] = path
g.graph['shortest_paths'] = all_shortest_paths

# function to compute the value of a given route on the graph
def compute_value(g, route):
  time = 26
  value = 0
  for source, dest in itertools.pairwise(['AA'] + route):
    time = time - len(g.graph['shortest_paths'][source][dest])
    if time <= 0: break
    value += max(time, 0) * g.nodes[dest]['flow']
  return value

# generator to reduce search space by culling paths longer than 26
def truncated_permutations(g, to_visit, parent_node='AA', remaining_distance=26):
  for i in range(len(to_visit)):
    this_node = to_visit[i]
    this_distance = len(g.graph['shortest_paths'][parent_node][this_node])
    if this_distance > remaining_distance and parent_node != 'AA': 
      yield []
    else:
      for perm in truncated_permutations(
        g,
        to_visit[:i] + to_visit[i+1:], 
        this_node,
        remaining_distance - this_distance - 1
      ): yield [this_node] + perm


counter = 0
max_val = 0
best_paths = [[], []]
to_visit = g.graph['to_visit']
to_visit_set = set(to_visit)

for path in truncated_permutations(g, to_visit):
  for complement in truncated_permutations(g, list(to_visit_set - set(path))):
    counter += 1
    val = compute_value(g, path) + compute_value(g, complement)
    if val > max_val: 
      max_val = val
      best_paths = path, complement
    if counter % 100000 == 0:
      print(counter)
      print(f'Best path so far has value {max_val}')
      print(f'Best path so far is {path} | {complement}')
      sys.stdout.flush()


print(f'Best path has value {max_val}')
print(f'Best path is {best_paths}')
print(counter)
