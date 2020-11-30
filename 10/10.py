#!/usr/bin/env python3

import sys
import math
import numpy as np

space = [line.strip() for line in sys.stdin]
height = len(space)
width = len(space[0])
best_seen = dict()
best_x, best_y = -1, -1
for y in range(height):
  for x in range(width):
    if space[y][x] != '#':
      continue
    seen = dict()
    for y1 in range(height):
      for x1 in range(width):
        if (x == x1 and y == y1) or space[y1][x1] != '#':
          continue
        dx = x1 - x
        dy = y1 - y
        d = math.gcd(dx, dy)
        dx //= d
        dy //= d
        key = '%d/%d' % (dx, dy)
        if key not in seen:
          seen[key] = (math.atan2(dx, dy), list())
        seen[key][1].append((x1, y1))
    if len(best_seen) < len(seen):
      best_seen = seen
      best_x = x
      best_y = y

print(len(best_seen))
print(best_x, best_y)

num = int(sys.argv[1])

values = list(sorted(best_seen.values(), key=lambda x: -x[0]))
print(values)
arc = sorted(values[num - 1][1], key=lambda p: (best_x - p[0])**2 + (best_y - p[1])**2)
print(arc)
res = arc[0]
print(res[0] * 100 + res[1])

