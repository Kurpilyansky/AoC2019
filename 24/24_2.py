#!/usr/bin/env python3

import sys
import re
import itertools

def get_on_border(dx, dy, i):
  x = abs(dx) * (2 - 2 * dx) + abs(dy) * i
  y = abs(dy) * (2 - 2 * dy) + abs(dx) * i
  return x, y

def get_neighbours(lvl, x, y):
  for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    nx, ny = x + dx, y + dy
    if (nx, ny) == (2, 2):
      for i in range(5):
        yield (lvl + 1, *get_on_border(dx, dy, i))
    elif 0 <= nx < 5 and 0 <= ny < 5:
      yield (lvl, nx, ny)
    else:
      yield (lvl - 1, 2 + dx, 2 + dy)


def gen_next(cur):
  neigh = dict()
  for pt in cur:
    for npt in get_neighbours(*pt):
      neigh[npt] = neigh.get(npt, 0) + 1
  return {pt for pt, cnt in neigh.items() if cnt == 1 or (cnt == 2 and pt not in cur)}


def main():
  a = sys.stdin.read().strip().split("\n")
  cur = set()
  for x in range(len(a)):
    for y in range(len(a[0])):
      if a[x][y] == '#':
        cur.add((0, x, y))

  iters = int(sys.argv[1])
  for i in range(iters):
    cur = gen_next(cur)
  print(len(cur))

if __name__ == "__main__":
  main()
