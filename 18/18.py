#!/usr/bin/env python3

import time
import os
import sys
import itertools
from queue import Queue


def parse():
  a = sys.stdin.read().strip().split('\n')
  return len(a), len(a[0]), a


n, m, a = parse()

nums = [[-1] * m for i in range(n)]
vert = []
edges = []
verts = 0
objects = dict()
for x in range(n):
  for y in range(m):
    if a[x][y] == '#':
      continue
    nums[x][y] = verts
    vert.append(None)
    edges.append([])
    verts += 1
    if a[x][y] != '.':
      objects[a[x][y]] = nums[x][y]
      vert[nums[x][y]] = a[x][y]

for x in range(n):
  for y in range(m):
    if a[x][y] == '#':
      continue
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
      x1 = x + dx
      y1 = y + dy
      if 0 <= x1 < n and 0 <= y1 < m and a[x1][y1] != '#':
        edges[nums[x][y]].append(nums[x1][y1])

keys = []
for i in range(26):
  ch = chr(ord('a') + i)
  if ch in objects:
    keys.append(ch)

K = len(keys)

def find_key_num(door_ch):
  for i in range(K):
    if ord(keys[i]) - ord('a') == ord(door_ch) - ord('A'):
      return i
  return K

def bfs(v, vert, edges, keys):
  n = len(edges)
  dist = [None] * n
  q = Queue()
  dist[v] = (0, 0)
  q.put(v)
  while not q.empty():
    v = q.get()
    for u in edges[v]:
      if dist[u] is None:
        d = dist[v][0] + 1
        door_mask = dist[v][1]
        if vert[u] and 'A' <= vert[u] <= 'Z':
          door_mask |= (1 << find_key_num(vert[u]))
        dist[u] = (d, door_mask)
        q.put(u)
  return dist

dist = [None] * verts
for ch, v in objects.items():
  dist[v] = bfs(v, vert, edges, keys)

print(objects)
dp = [dict() for i in range(K)]
for i in range(K):
  x = dist[objects['@']][objects[keys[i]]]
  if x[1] == 0:
    dp[i][1 << i] = x[0]


for mask in range(1, 1 << K):
  if mask % 100000 == 0:
    print(mask)
  for last in range(K):
    if mask not in dp[last]:
      continue
    #print('dp[last %d][mask %d] = %d' % (last, mask, dp[last][mask]))
    for j in range(K):
      if (mask & (1 << j)) != 0:
        continue
      x = dist[objects[keys[last]]][objects[keys[j]]]
      if (x[1] & mask) == x[1]:
        new_mask = mask | (1 << j)
        new_val = dp[last][mask] + x[0]
        if new_mask not in dp[j] or dp[j][new_mask] > new_val:
          dp[j][new_mask] = new_val

#print(dp)

res = 2**30
all_mask = (1 << K) - 1
for last in range(K):
  if all_mask in dp[last]:
    res = min(res, dp[last][all_mask])
print(res)

