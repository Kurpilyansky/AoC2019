#!/usr/bin/env python3

import sys

INF = 10 ** 9

def read_wire():
  def process_seg(point, pref_sum, seg):
    dirs = {"R": (1, 0),
            "L": (-1, 0),
            "U": (0, 1),
            "D": (0, -1)}
    length = int(seg[1:])
    delta = dirs[seg[0]]
    return (point[0] + delta[0] * length, point[1] + delta[1] * length), pref_sum + length

  segs = input().split(',')
  points = [(0, 0)]
  pref_sums = [0]
  for seg in segs:
    point, pref_sum = process_seg(points[-1], pref_sums[-1], seg)
    points.append(point)
    pref_sums.append(pref_sum)
    
  return points, pref_sums


def dist(p1, p2):
  return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def find_intersection(p1, p2, pref_len1, p3, p4, pref_len2):
  mins = tuple(max(min(p1[i], p2[i]), min(p3[i], p4[i])) for i in range(2))
  maxs = tuple(min(max(p1[i], p2[i]), max(p3[i], p4[i])) for i in range(2))
  if mins[0] > maxs[0] or mins[1] > maxs[1]:
    return INF, INF
  if mins[0] == maxs[0] and mins[1] == maxs[1]:
    return dist((0, 0), mins), pref_len1 + pref_len2 + dist(p1, mins) + dist(p3, mins)
  else:
    print(mins, maxs)
    raise ValueError('zz')


w1, sum1 = read_wire()
w2, sum2 = read_wire()

res1 = INF
res2 = INF
for i1 in range(len(w1) - 1):
  for i2 in range(len(w2) - 1):
    if i1 != 0 or i2 != 0:
      d1, d2 = find_intersection(w1[i1], w1[i1 + 1], sum1[i1], w2[i2], w2[i2 + 1], sum2[i2])
      res1 = min(res1, d1)
      res2 = min(res2, d2)
print(res1)
print(res2)

