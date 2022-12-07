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

used_space = du(fs)
total_space = 70000000
update_size = 30000000
available_space = total_space - used_space
delete_size = update_size - available_space
print(f'Root dir size: {used_space}')
print(f'Available space: {available_space}')
print(f'Need to free up: {delete_size}')


big_enough = []
def traverse_tree(node, indent=''):
  global big_enough
  global delete_size
  for k, v in node.items():
    if type(v) != dict:
      if v >= delete_size:
        big_enough.append(v)
        print(f'DEBUG] {indent}{k} {v}')
    else:
      size = du(v)
      if size >= delete_size:
        big_enough.append(size)
        print(f'DEBUG] {indent}{k} {size}')
      traverse_tree(v, f'{indent}  ')
traverse_tree(fs)

big_enough.sort()
print(big_enough[0])
