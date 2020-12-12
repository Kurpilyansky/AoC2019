#!/usr/bin/env python3

import time
import os
import sys
import itertools
from Intcode import *

class TractorBeam:
  def __init__(self, prog_code):
    self._prog_code = prog_code

  def check(self, x, y):
    prog = Program(prog_code, [x, y])
    out = prog.run()
    print(x, y, out)
    return out[0] == 1

 
prog_code = parse_prog_code(sys.argv[1])
beam = TractorBeam(prog_code)
count = 0
for x in range(50):
  break
  s = ''
  for y in range(50):
    if beam.check(x, y):
      s += '#'
      count += 1
    else:
      s += '.'
  print(s)
print(count)


yL = 0
yR = 0
SIZE = 100
x = SIZE
bounds = []
while x <= 10000:
  while not beam.check(x, yL):
    yL += 1
  yR = max(yR, yL)
  while beam.check(x, yR):
    yR += 1
  bounds.append((yL, yR))
  print(x, [yL, yR], len(bounds))
  x += 1

  if len(bounds) >= SIZE:
    print(bounds[-SIZE], bounds[-1])
    if bounds[-SIZE][1] - SIZE >= bounds[-1][0]:
      print(x - SIZE, bounds[-1][0])
      print((x - SIZE) * 10000 + bounds[-1][0])
      break

