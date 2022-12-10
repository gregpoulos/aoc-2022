#!/usr/local/bin/python3

class Cpu(object):
  """docstring for Cpu"""
  def __init__(self, timer):
    self.x = 1
    self.timer = timer

  def addx(self, x):
    # print(f'adding x = {x}')
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

  def get_cycle(self):
    return self.timer.t

  def __str__(self):
    return f'CPU{{{x}}}'


class Timer(object):
  """docstring for Timer"""
  def __init__(self):
    self.t = 0

  def register(self, monitor):
    self.monitor = monitor

  def inc(self):
    self.t += 1
    if self.is_interesting():
      self.monitor.increase_signal()

  def is_interesting(self):
    return self.t == 20 or (self.t - 20) % 40 == 0


class Monitor(object):
  """docstring for Monitor"""
  def __init__(self, cpu):
    self.val = 0
    self.cpu = cpu
    cpu.timer.register(self)
  
  def increase_signal(self):
    self.val += self.cpu.timer.t * self.cpu.x
  

cpu = Cpu(Timer())
monitor = Monitor(cpu)
for line in open('input.txt', 'r').readlines():
  cpu.exec(line.strip())
print(monitor.val)
