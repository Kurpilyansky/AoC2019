#!/usr/bin/env python3

import sys
import re
import itertools

def gen_next(cur):
  neigh = dict()
  for pt in cur:
    for dpt in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      npt = tuple(map(sum, zip(pt, dpt)))
      if 0 <= npt[0] < 5 and 0 <= npt[1] < 5:
        neigh[npt] = neigh.get(npt, 0) + 1
  return {pt for pt, cnt in neigh.items() if cnt == 1 or (cnt == 2 and pt not in cur)}


def calc_val(cur):
  return sum(map(lambda p: (1 << (p[0] * 5 + p[1])), cur))

def main():
  a = sys.stdin.read().strip().split("\n")
  cur = set()
  for x in range(len(a)):
    for y in range(len(a[0])):
      if a[x][y] == '#':
        cur.add((x, y))

  used = set()
  while True:
    val = calc_val(cur)
    if val in used:
      break
    used.add(val)
    cur = gen_next(cur)
  print(val)

if __name__ == "__main__":
  main()
