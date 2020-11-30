#!/usr/bin/env python3

import time
import os
import sys
import itertools

class Reagent:
  def __init__(self, s):
    x, y = s.split(' ')
    self.cnt = int(x)
    self.chemical = y

class Reaction:
  def __init__(self, s):
    ins, out = s.split(' => ')
    self.inputs = list([Reagent(x) for x in ins.split(', ')])
    self.output = Reagent(out)

reactions = [Reaction(line.strip()) for line in sys.stdin]
reactions = {r.output.chemical: r for r in reactions}

def dfs(v, used, topsort):
  if v in used or v == 'ORE':
    return
  used.add(v)
  for inp in reactions[v].inputs:
    dfs(inp.chemical, used, topsort)
  topsort.append(v)

fin = 'FUEL'
topsort = []
dfs(fin, set(), topsort)

def get_needed_ore(cnt):
  amounts = {'FUEL': cnt}
  for v in topsort[::-1]:
    react = reactions[v]
    need = (amounts[v] + react.output.cnt - 1) // react.output.cnt
    for inp in react.inputs:
      if inp.chemical not in amounts:
        amounts[inp.chemical] = 0
      amounts[inp.chemical] += need * inp.cnt
  return amounts['ORE']

needed_for_one = get_needed_ore(1)
print(needed_for_one)

CNT = 10**12
L = 0
R = CNT
while L + 1 < R:
  M = (L + R) // 2
  if get_needed_ore(M) > CNT:
    R = M
  else:
    L = M
print(L)


