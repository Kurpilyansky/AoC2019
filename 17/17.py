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
  return ''.join(map(chr, ints))


def encode(s):
  return list(map(ord, s))


def get_camera_view(prog_code):
  prog = Program(prog_code, [])
  out = decode(prog.run())
  print(out)
  image = out.strip().split('\n')
  return len(image), len(image[0]), image


def run_robot(prog_code, text):
  prog_code = list(prog_code)
  prog_code[0] = 2
  prog = Program(prog_code, encode(text))
  out = prog.run()
  res = out[-1]
  out = decode(out[:-1])
  print(out)
  return res
  


def calc_alignment_params(n, m, image):
  res = 0
  for x in range(n):
    for y in range(m):
      if image[x][y] == '.':
        continue
      count = 0
      if x != 0 and image[x - 1][y] != '.':
        count += 1
      if y != 0 and image[x][y - 1] != '.':
        count += 1
      if x != n - 1 and image[x + 1][y] != '.':
        count += 1
      if y != m - 1 and image[x][y + 1] != '.':
        count += 1
      if count >= 3:
        res += x * y
  return res


def find(n, m, image, ch):
  for x in range(n):
    for y in range(m):
      if image[x][y] == ch:
        return x, y


def find_path(n, m, image):
  dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
  x, y = find(n, m, image, '^')
  dir_ = 0
  path = []
  while True:
    ok = False
    for i in [1, 3]:
      new_dir = (dir_ + i) % 4
      x1 = x + dirs[new_dir][0]
      y1 = y + dirs[new_dir][1]
      if 0 <= x1 < n and 0 <= y1 < m and image[x1][y1] == '#':
        path.append('R' if i == 1 else 'L')
        dir_ = new_dir
        ok = True
        break
    if not ok:
      break
    
    cnt = 0
    while True:
      x1 = x + dirs[new_dir][0]
      y1 = y + dirs[new_dir][1]
      if 0 <= x1 < n and 0 <= y1 < m and image[x1][y1] == '#':
        x, y = x1, y1
        cnt += 1
      else:
        break
    path.append(cnt)
  return path


prog_code = parse_prog_code(sys.argv[1])
n, m, image = get_camera_view(prog_code)
print(calc_alignment_params(n, m, image))

MAX_LEN = 20
path = find_path(n, m, image)
print(path)

class FindAnswer(Exception):
  def __init__(self, ans):
    self.ans = ans


def brute(path, prog, sub_progs):
  if len(prog) * 2 - 1 > MAX_LEN:
    return

  if len(path) == 0:
    raise FindAnswer((prog, sub_progs))

  for i in range(len(sub_progs)):
    sub_prog = sub_progs[i]
    if path[:len(sub_prog)] == sub_prog:
      prog.append(chr(ord('A') + i))
      brute(path[len(sub_prog):], prog, sub_progs)
      prog.pop()
  if len(sub_progs) == 3:
    return
  for i in range(1, len(path) + 1):
    sub_prog = path[:i]
    if len(','.join(map(str, sub_prog))) > MAX_LEN:
      break

    prog.append(chr(ord('A') + len(sub_progs)))
    sub_progs.append(sub_prog)
    brute(path[i:], prog, sub_progs)
    sub_progs.pop()
    prog.pop()


try:
  brute(path, [], [])
except FindAnswer as e:
  print(e.ans)
  text = ''
  text += ','.join(e.ans[0]) + '\n'
  for x in e.ans[1]:
    text += ','.join(map(str, x)) + '\n'
  text += 'y\n'
  print(text)
  print(run_robot(prog_code, text))
