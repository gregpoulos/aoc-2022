#!/usr/local/bin/python3

import networkx as nx
import re
import itertools
import random
import sys


# def int_log2(i):
#   val = -1
#   while i > 0:
#     i = i >> 1
#     val += 1
#   return val

# def bitmasks(i):
#   mask_length = int_log2(i) + 1
#   for this in range(i):
#     mask = []
#     for bit in range(mask_length):
#       mask.append(1 if this & (1 << bit) else 0)
#     yield mask

# def permutations(lst):
#   if len(lst) == 1: 
#     yield lst
#   elif len(lst) > 1:
#     for i in range(len(lst)):
#       for perm in permutations(lst[:i]+lst[i+1:], depth+1):
#         yield [lst[i]] + perm
#   # else: ignore empty lists


g = nx.Graph()
g.graph['to_visit'] = []
for line in open('input.txt', 'r').readlines():
  valve, *neighbors = re.findall(r"[A-Z][A-Z]", line)
  flow = int(re.search(r"[0-9]+", line).group())
  if flow > 0:
    g.graph['to_visit'].append(valve)
  g.add_node(valve, flow=flow)
  g.add_edges_from([(valve, n) for n in neighbors])

all_shortest_paths = {}
for source, dests in nx.all_pairs_shortest_path(g):
  all_shortest_paths[source] = {}
  for dest, path in dests.items():
    all_shortest_paths[source][dest] = path
g.graph['shortest_paths'] = all_shortest_paths

# def compute_value(g, routes):
#   agents = []
#   for route in routes:
#     if route == []: return 0
#     agents.append({ 
#       'location': 'AA',
#       'destination': route[0],
#       'path': nx.shortest_path(g, 'AA', route[0])[1:], 
#       'itinerary': route[1:]
#     })
#   agents[0]['name'] = '1'
#   # agents[1]['name'] = '2'
#   time = 30
#   score = 0
#   opened_valves = set()
#   while time > 0:
#     for v in opened_valves:
#       # if v in g.graph['to_visit']: print(f'Valve {v} is open for a pressure release of {g.nodes[v]["flow"]}')
#       score += g.nodes[v]['flow']

#     for agent in agents:
#       # agent has reached a valve
#       if agent['destination'] == agent['location']:
#         # if agent['location'] in g.graph['to_visit']: print(f'Agent {agent["name"]} is opening valve at {agent["location"]}')
#         opened_valves.add(agent['location'])
#         if any(agent['itinerary']):
#           agent['destination'] = agent['itinerary'].pop(0)
#           agent['path'] = nx.shortest_path(g, agent['location'], agent['destination'])

#       # agent makes a move
#       # Note: The first element of the path returned by nx.shortest_path() 
#       # is the current node, so if the agent opened a valve this turn, this
#       # is a no-op (which is exactly what we want).
#       if any(agent['path']):
#         # if agent['location'] != agent['path'][0]: print(f'Agent {agent["name"]} is stepping to valve {agent["location"]}')
#         agent['location'] = agent['path'].pop(0)

#     # print(f'--END MINUTE {time}--')
#     time -= 1
#   return score


def compute_value(g, route):
  time = 26
  value = 0
  full_route = ['AA'] + route
  for i in range(len(full_route)-1):
    source = full_route[i]
    dest = full_route[i+1]
  # for source, dest in itertools.pairwise(['AA'] + route):
    time = time - len(g.graph['shortest_paths'][source][dest])
    if time <= 0: break
    value += max(time, 0) * g.nodes[dest]['flow']
  return value


counter = 0
max_val = 0
best_path = []
to_visit = g.graph['to_visit']

# for path in itertools.permutations(['VB', 'KR', 'OT', 'BT', 'YX', 'OF', 'RR']):
#   val = compute_value(g, list(path))
#   if val > max_val: 
#     max_val = val
#     best_path = list(path)
#   counter += 1
#   if counter % 1000000 == 0:
#     print(f'On iteration {counter}')
#     print(f'Maximum value so far is {max_val}')
#     print(f'Best path so far is {best_path}')


tried = set()
while True:
  to_visit.sort(key=lambda n: -random.random() * g.nodes[n]['flow'])
  agent1, agent2 = [], []
  for n in to_visit:
    agent1.append(n) if random.randint(0, 1) else agent2.append(n)

  this_hash = ''.join(agent1) + '|' + ''.join(agent2)
  if this_hash in tried: continue

  val = compute_value(g, agent1) + compute_value(g, agent2)
  tried.add(this_hash)

  if val > max_val: 
    max_val = val
    best_path = [agent1, agent2]
  counter += 1
  if counter % 100000 == 0:
    print(f'Maximum value so far is {max_val}')
    print(f'Best path so far is {best_path[0]}, {best_path[1]}')
    sys.stdout.flush()

print(f'Best path has value {max_val}')
print(f'Best path is {best_path}')
