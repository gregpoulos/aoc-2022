#!/usr/local/bin/python3

def decrypt(x):
  return {
    'A': 'r',
    'B': 'p',
    'C': 's',
  }[x]

point_values = {
  'r': 1,
  'p': 2,
  's': 3,
  'X': 0,
  'Y': 3,
  'Z': 6
}

def beats(x):
  if x == 'r':
    return 'p'
  elif x == 'p':
    return 's'
  else:
    return 'r'

def loses_to(x):
  return beats(beats(x))

def compute_move(opp, result):
  if result == 'Z':
    return beats(opp)
  elif result == 'Y':
    return opp
  else:
    return loses_to(opp)

score = 0
for line in open('guide.txt', 'r').readlines():
  opp, result = line.strip().split(' ')
  score += point_values[result]
  score += point_values[compute_move(decrypt(opp), result)]
print(score)
