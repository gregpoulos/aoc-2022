#!/usr/local/bin/python3

import sys

fn = 'test.txt'
if len(sys.argv) > 1:
  fn = sys.argv[1]

def char_to_value(c):
  if c == '-': return -1
  if c == '=': return -2
  return int(c)

def value_to_char(v):
  if v == -1: return '-'
  if v == -2: return '='
  return str(v)

def padded(x, y):
  if len(x) < len(y): return '0'*(len(y)-len(x))+x, y
  if len(y) < len(x): return x, '0'*(len(x)-len(y))+y
  return x, y

def snafu_sum(x, y):
  x, y = padded(x, y)
  carry, result = 0, []
  for d1, d2 in zip(map(char_to_value, reversed(x)), map(char_to_value, reversed(y))):
    _sum = d1 + d2 + carry
    carry = 0
    if abs(_sum) > 2: carry = 1 if _sum > 0 else -1
    _sum -= carry*5
    result.append(value_to_char(_sum))
  if carry != 0: result.append(value_to_char(carry))
  return ''.join(reversed(result))

def snafu_to_dec(snafu):
  dec = 0
  for n, d in enumerate(reversed(snafu)):
    place = 5 ** n
    if d == '-': dec -= place
    elif d == '=': dec -= 2 * place
    else: dec += int(d) * place
  return dec

val = '0'
for line in open(fn, 'r').readlines():
  val = snafu_sum(val, line.strip())
print(val)
