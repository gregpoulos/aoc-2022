#!/usr/local/bin/python3

def decrypt(x):
  return {
    'A': 'r',
    'B': 'p',
    'C': 's',
    'X': 'r',
    'Y': 'p',
    'Z': 's',
  }[x]

point_values = {
  'r': 1,
  'p': 2,
  's': 3
}

def play_match(me, opp):
  if (me == 'r' and opp == 's') or (me == 's' and opp == 'p') or (me == 'p' and opp == 'r'):
    return 6
  elif (me == opp):
    return 3
  else:
    return 0

score = 0
for line in open('guide.txt', 'r').readlines():
  opp, me = map(decrypt, line.strip().split(' '))
  score += point_values[me]
  score += play_match(me, opp)
print(score)
