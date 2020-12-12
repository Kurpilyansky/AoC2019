#!/usr/bin/env python3

import time
import os
import sys
import itertools
from Intcode import *

UNKNOWN = 0
EMPTY = 1
WALL = 2
DROID = 3

class TargetFoundException(Exception):
  pass

class Cell:
  def __init__(self):
    self.parent = None
    self.dir_from_parent = None
    self.depth = None
    self.value = UNKNOWN

class Field:
  def __init__(self):
    self._c = dict()
    self._minx = 0
    self._maxx = 0
    self._miny = 0
    self._maxy = 0

  def get(self, x, y):
    self._minx = min(self._minx, x)
    self._maxx = max(self._maxx, x)
    self._miny = min(self._miny, y)
    self._maxy = max(self._maxy, y)
    if x not in self._c:
      self._c[x] = dict()
    if y not in self._c[x]:
      self._c[x][y] = Cell()
    return self._c[x][y]

  def show(self):
    def show_char(val):
      if val == EMPTY:
        return '.'
      if val == WALL:
        return '#'
      if val == DROID:
        return 'D'
      return ' '

    for x in range(self._minx, self._maxx + 1):
      s = ''
      for y in range(self._miny, self._maxy + 1):
        s += show_char(self.get(x, y).value)
      print(s)


def sign(x):
  if x > 0:
    return 1
  if x < 0:
    return -1
  return 0

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def get_neigh(pos, direction):
  return (pos[0] + dx[direction], pos[1] + dy[direction])

class Droid:
  def __init__(self, prog_code):
    self._prog = Program(prog_code, [])
    self._field = Field()
    self._pos = (0, 0)

    start_cell = self._field.get(*self._pos)
    start_cell.value = DROID
    start_cell.depth = 0

    self._field.get(-10, -10).value = UNKNOWN

  def _move(self, direction):
    self._prog.put_input(direction + 1)
    out = self._prog.run()[0]
    #print('move', direction, out)
    new_pos = get_neigh(self._pos, direction)
    if out == 0:
      self._field.get(*new_pos).value = WALL
    elif out == 1 or out == 2:
      self._field.get(*self._pos).value = EMPTY
      self._pos = new_pos
      self._field.get(*self._pos).value = DROID

    os.system('clear')
    self._field.show()
    return out

  def _go(self, target_pos):
    #print('go', target_pos)
    prefix = []
    suffix = []
    start = self._pos
    end = target_pos
    while start[0] != end[0] or start[1] != end[1]:
      start_cell = self._field.get(*start)
      end_cell = self._field.get(*end)
      d1 = start_cell.depth
      d2 = end_cell.depth
      if d1 >= d2:
        prefix.append(start_cell.dir_from_parent ^ 1)
        start = start_cell.parent
      if d1 <= d2:
        suffix.append(end_cell.dir_from_parent)
        end = end_cell.parent
    #print(prefix, suffix)
    prefix += suffix[::-1]
    for direction in prefix:
      self._move(direction)
    if self._pos[0] != target_pos[0] or self._pos[1] != target_pos[1]:
      raise ValueError()

  def run(self):
    self._field.show()
    curD = 0
    droid_start_pos = self._pos
    oxygen_pos = None
    q = [self._pos]
    while q:
      pos = q[-1]
      q.pop()
      for direction in range(4):
        new_pos = get_neigh(pos, direction)
        #print(new_pos)
        self._go(pos)
        if self._field.get(*new_pos).value != UNKNOWN:
          continue
        res = self._move(direction)
        if res == 2:
          oxygen_pos = new_pos
        if res == 1 or res == 2:
          cur_cell = self._field.get(*pos)
          next_cell = self._field.get(*new_pos)
          next_cell.depth = cur_cell.depth + 1
          next_cell.parent = pos
          next_cell.dir_from_parent = direction
          q.append(new_pos)

    print(self._bfs(droid_start_pos, oxygen_pos))
    print(self._bfs(oxygen_pos))

  def _bfs(self, start_pos, end_pos=None):
    used = set()
    q0 = [start_pos]
    used.add(start_pos)
    curD = 0
    while q0:
      q1 = []
      for pos in q0:
        if pos == end_pos:
          return curD
        for direction in range(4):
          new_pos = get_neigh(pos, direction)
          if self._field.get(*new_pos).value != WALL and new_pos not in used:
            q1.append(new_pos)
            used.add(new_pos)
      q0 = q1
      curD += 1
    return curD - 1

prog_code = parse_prog_code(sys.argv[1])
Droid(prog_code).run()
