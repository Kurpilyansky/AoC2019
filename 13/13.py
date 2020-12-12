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

def sign(x):
  if x > 0:
    return 1
  if x < 0:
    return -1
  return 0

class Arcade:
  def __init__(self, prog_code):
    prog_code[0] = 2
    self._prog = Program(prog_code, [])

  def run(self):
    score = 0
    field = Field()
    while not self._prog.is_halted():
      out = self._prog.run()
      for i in range(0, len(out), 3):
        x, y, val = out[i], out[i + 1], out[i + 2]
        if x == -1 and y == 0:
          score = val
        else:
          field.set(y, x, val)
      os.system('clear')
      print('Score: %d' % score)
      field.show()

      paddle_pos = field.find(3)
      ball_pos = field.find(4)
      self._prog.put_input(sign(ball_pos[1] - paddle_pos[1]))
      time.sleep(0.01)
    return score

prog_code = parse_prog_code(sys.argv[1])
arcade = Arcade(prog_code)
arcade.run()
