#!/usr/bin/env python3

import sys
import itertools
import re
import math

def sign(x):
  if x > 0:
    return 1
  if x < 0:
    return -1
  return 0


class Vector:
  def __init__(self, xs):
    self.xs = xs

  def energy(self):
    return sum(map(abs, self.xs))

  def __repr__(self):
    return '<x=%d, y=%d, z=%d>' % tuple(self.xs)


class Moon:
  def __init__(self, s):
    m = re.match(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", s)
    x, y, z = map(lambda i: int(m.group(i)), range(1, 4))
    self.position = Vector([x, y, z])
    self.velocity = Vector([0, 0, 0])

  def adjust_velocity(self, other_pos):
    for i in range(3):
      self.velocity.xs[i] += sign(other_pos.xs[i] - self.position.xs[i])    

  def adjust_position(self):
    for i in range(3):
      self.position.xs[i] += self.velocity.xs[i]

  def total_energy(self):
    return self.position.energy() * self.velocity.energy()
  
  def __repr__(self):
    return '[pos=' + str(self.position) + ', vel=' + str(self.velocity) + ']'


class Cycle:
  def __init__(self, pred, cycle):
    print(pred, cycle)
    self.pred = pred
    self.cycle = cycle

  def merge(self, other):
    self.pred = max(self.pred, other.pred)
    self.cycle *= other.cycle // math.gcd(self.cycle, other.cycle)

class CycleFinder:
  def __init__(self, i):
    self._iter = 0
    self._index = i
    self._cache = dict()

  def add_new_state(self, moons):
    keys = []
    for m in moons:
      keys.append(m.position.xs[self._index])
      keys.append(m.velocity.xs[self._index])
    key = ','.join(map(str, keys))
    if key not in self._cache:
      self._cache[key] = self._iter
      self._iter += 1
      return None

    return Cycle(self._cache[key], self._iter - self._cache[key])

moons = list([Moon(line.strip()) for line in sys.stdin])
iters = int(sys.argv[1])
finders = {i: CycleFinder(i) for i in range(3)}
tot_cycle = Cycle(0, 1)
i = 0
while i <= iters or finders:
  for m1 in moons:
    for m2 in moons:
      m1.adjust_velocity(m2.position)
  for m1 in moons:
    m1.adjust_position()

  for j, finder in list(finders.items()):
    cur_cycle = finder.add_new_state(moons)
    if cur_cycle:
      tot_cycle.merge(cur_cycle)
      del finders[j]

  if i == iters:
    print(sum(map(lambda x: x.total_energy(), moons)))

  i += 1

print(tot_cycle.pred + tot_cycle.cycle)
