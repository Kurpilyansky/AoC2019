#!/usr/bin/env python3

import time
import os
import sys
import itertools
from queue import Queue


def parse():
  a = sys.stdin.read().strip('\n').split('\n')
  return len(a), len(a[0]), a


n, m, a = parse()
print(n, m)
print('\n'.join(a))

nums = [[-1] * m for i in range(n)]
edges = []
verts = 0
objects = dict()
portals = dict()
for x in range(n):
  for y in range(m):
    if a[x][y] != '.':
      continue
    nums[x][y] = verts
    edges.append([])
    verts += 1
    if a[x][y] != '.':
      objects[a[x][y]] = nums[x][y]

for x in range(n):
  for y in range(m):
    if a[x][y] != '.':
      continue
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      x1 = x + dx
      y1 = y + dy
      if 0 <= x1 < n and 0 <= y1 < m:
        if a[x1][y1] == '.':
          edges[nums[x][y]].append((0, nums[x1][y1]))
        elif a[x1][y1] != '#' and a[x1][y1] != ' ':
          x2 = x1 + dx
          y2 = y1 + dy
          portal = ''.join(map(lambda x: x[2], sorted([(x1, y1, a[x1][y1]), (x2, y2, a[x2][y2])])))
          if portal not in portals:
            portals[portal] = [None, None]
          if x == 2 or y == 2 or x == n - 3 or y == m - 3:
            portals[portal][0] = nums[x][y]
          else:
            portals[portal][1] = nums[x][y]

for portal, vs in portals.items():
  if vs[0] is not None and vs[1] is not None:
    edges[vs[0]].append((-1, vs[1]))
    edges[vs[1]].append((1, vs[0]))


def bfs(v, edges):
  n = len(edges)
  dist = [None] * n
  q = Queue()
  dist[v] = 0
  q.put(v)
  while not q.empty():
    v = q.get()
    for _, u in edges[v]:
      if dist[u] is None:
        dist[u] = dist[v] + 1
        q.put(u)
  return dist

dist = bfs(portals['AA'][0], edges)
print(dist[portals['ZZ'][0]])


def bfs2(s, f, edges):
  n = len(edges)
  dist = []
  dist.append([None] * n)
  q = Queue()
  dist[0][s] = 0
  q.put((0, s))
  while not q.empty():
    lvl, v = q.get()
    if lvl == 0 and v == f:
      return dist[0][f]
    for dlvl, u in edges[v]:
      nlvl = lvl + dlvl
      if nlvl < 0:
        continue
      if nlvl >= len(dist):
        dist.append([None] * n)
      if dist[nlvl][u] is None:
        dist[nlvl][u] = dist[lvl][v] + 1
        q.put((nlvl, u))

print(bfs2(portals['AA'][0], portals['ZZ'][0], edges))

