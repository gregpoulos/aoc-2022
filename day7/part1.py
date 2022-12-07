#!/usr/local/bin/python3
from pprint import pprint

fs = {}
pwd = []

def parse_line(line):
  print(line)
  if (line[0] == '$'): # execute command
    execute(line[2:])
  else: # read from stout
    filetype, filename = line.split(' ')
    if filetype == 'dir':
      add_to_fs(filename, {})
    else:
      add_to_fs(filename, int(filetype))


def execute(cmd):
  global pwd
  if cmd == 'ls':
    return
  # else fn == 'dir x'
  arg = cmd.split(' ')[1]
  if arg == '/':
    pwd = []
  elif arg == '..':
    pwd.pop()
  else:
    pwd.append(arg)


def add_to_fs(fn, size):
  global fs
  global pwd
  here = fs
  for x in pwd:
    here = here[x]
  here[fn] = size


for line in open('input.txt', 'r').readlines():
  parse_line(line.strip())


def du(node):
  if type(node) != dict:
    return node
  return sum([du(child) for child in node.values()])

result = 0
def traverse_tree(node, indent=''):
  global result
  for k, v in node.items():
    if type(v) != dict:
      if v <= 100000:
        print(f'DEBUG] {indent}{k} {v}')
    else:
      size = du(v)
      if size <= 100000:
        print(f'DEBUG] {indent}{k} {size}')
        result += size
      traverse_tree(v, f'{indent}  ')

traverse_tree(fs)
print(result)