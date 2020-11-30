#!/usr/bin/env python3

import sys

def get_depth(x, parent, depth):
  if x in depth:
    return depth[x]
  if x not in parent:
    depth[x] = 0
  else:
    depth[x] = get_depth(parent[x], parent, depth) + 1
  return depth[x]

def find_lca(x, y):
  while depth[x] > depth[y]:
    x = parent[x]
  while depth[x] < depth[y]:
    y = parent[y]
  while x != y:
    x = parent[x]
    y = parent[y]
  return x

parent = dict()
depth = dict()

for line in sys.stdin:
  a, b = line.strip().split(')')
  parent[b] = a

res = 0
for x in parent.keys():
  res += get_depth(x, parent, depth)
print(res)

s = 'YOU'
t = 'SAN'
print(depth[s] + depth[t] - 2 * depth[find_lca(s, t)] - 2)

