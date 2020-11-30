#!/usr/bin/env python3

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
    for x in range(self._minx, self._maxx + 1):
      s = ''
      for y in range(self._miny, self._maxy + 1):
        s += '#' if self.get(x, y) == 1 else ' '
      print(s)


class Robot:
  def __init__(self, prog_code, val):
    self._prog = Program(prog_code, [])
    self._x = 0
    self._y = 0
    self._dir = 0
    self._field = Field()

    self._dx = [-1, 0, 1, 0]
    self._dy = [0, -1, 0, 1]

    self._set_cur_color(val)

  def run(self):
    while not self._prog.is_halted():
      self._prog.put_input(self._get_cur_color())
      out = self._prog.run()
      self._set_cur_color(out[0])
      self._turn(out[1])
      self._move()
    self._field.show()
    print(self._field.count())

  def _get_cur_color(self):
    return self._field.get(self._x, self._y)

  def _set_cur_color(self, val):
    return self._field.set(self._x, self._y, val)

  def _turn(self, direction):
    self._dir = (self._dir + 1 + direction * 2) % 4

  def _move(self):
    self._x += self._dx[self._dir]
    self._y += self._dy[self._dir]


prog_code = parse_prog_code(sys.argv[1])
Robot(prog_code, 0).run()
Robot(prog_code, 1).run()

