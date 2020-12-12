#!/usr/bin/env python3

import time
import os
import sys
import itertools
from Intcode import *

class Field:
  def __init__(self):
    self._c = dict()
    self._minx = 0
    self._maxx = 0
    self._miny = 0
    self._maxy = 0

  def get(self, x, y):
    if x not in self._c:
      return 0
    return self._c[x].get(y, 0)

  def set(self, x, y, val):
    if x not in self._c:
      self._c[x] = dict()
    self._c[x][y] = val
    self._minx = min(self._minx, x)
    self._maxx = max(self._maxx, x)
    self._miny = min(self._miny, y)
    self._maxy = max(self._maxy, y)

  def count(self):
    return sum([len(t) for t in self._c.values()])

  def show(self):
    def show_char(val):
      return [' ', '#', '.', '*', 'o'][val]

    for x in range(self._minx, self._maxx + 1):
      s = ''
      for y in range(self._miny, self._maxy + 1):
        s += show_char(self.get(x, y))
      print(s)

  def find(self, val):
    for x, v in self._c.items():
      for y, z in v.items():
        if z == val:
          return x, y

def decode(ints):
  def dec(i):
    if i < 256:
      return chr(i)
    else:
      return str(i)

  return ''.join(map(dec, ints))


def encode(s):
  return list(map(ord, s))


def run_droid(prog_code, commands):
  prog_code = list(prog_code)
  text = '\n'.join(commands) + '\n'
  prog = Program(prog_code, encode(text))
  out = prog.run()
  out = decode(out)
  print(out)
  

prog_code = parse_prog_code(sys.argv[1])


commands = []
commands.append('NOT T T')
regs = 'ABCD'
for i in range(3):
  commands.append('AND %s T' % regs[i])
commands.append('NOT T J')
commands.append('AND D J')
commands.append('WALK')
print(commands)
run_droid(prog_code, commands)

commands = []
regs = 'ABCDEFGHI'
commands.append('OR H J')
commands.append('OR E T')
commands.append('AND I T')
commands.append('OR T J')
commands.append('NOT A T')
commands.append('OR A T')
for i in range(3):
  commands.append('AND %s T' % regs[i])
commands.append('NOT T T')
commands.append('AND T J')
commands.append('AND D J')
commands.append('NOT A T')
commands.append('OR T J')
commands.append('RUN')
print(commands)
run_droid(prog_code, commands)

