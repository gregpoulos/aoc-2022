#!/usr/local/bin/python3

class Timer(object):
  """docstring for Timer"""
  def __init__(self):
    self.t = 0

  def register(self, crt):
    self.crt = crt

  def inc(self):
    self.t += 1
    self.crt.print_t(self.t)


class Cpu(object):
  """docstring for Cpu"""
  def __init__(self, timer=Timer()):
    self.x = 1
    self.timer = timer

  def addx(self, x):
    self.timer.inc()
    self.timer.inc()
    self.x += x

  def noop(self):
    self.timer.inc()
    return

  def exec(self, cmd):
    if cmd == 'noop':
      self.noop()
    else:
      self.addx(int(cmd.split(' ')[1]))

  def register(self, crt):
    self.crt = crt
    self.timer.register(crt)

  def get_cycle(self):
    return self.timer.t

  def __str__(self):
    return f'CPU{{{x}}}'


class Crt(object):
  SIZE = 240
  LINE_LENGTH = 40

  """docstring for Crt"""
  def __init__(self, cpu):
    self.display = [False] * Crt.SIZE
    self.cpu = cpu
    cpu.register(self)

  def print_t(self, t):
    idx = t % self.LINE_LENGTH - 1
    sprite = self.cpu.x
    self.display[idx] = idx in range(sprite-1, sprite+2)
    self.draw_1(idx)
  
  def draw_1(self, idx):
    # print(f'DEBUG] drawing character at index {idx}: ')
    print('#' if self.display[idx] else '.', end='')
    if (idx+1) % Crt.LINE_LENGTH == 0:
      print('\n', end='')

  def draw_all(self):
    for i in range(Crt.SIZE):
      self.draw_1(i)
      

cpu = Cpu()
crt = Crt(cpu)
for line in open('input.txt', 'r').readlines():
  cpu.exec(line.strip())
