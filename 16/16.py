#!/usr/bin/env python3

import time
import os
import sys
import itertools


def next_phase(s):
  coefs = [0, 1, 0, -1]
  t = ''
  for i in range(len(s)):
    x = 0
    for j in range(len(s)):
      x += int(s[j]) * coefs[(j + 1) // (i + 1) % 4]
    t += str(x)[-1]
  return t


def next_phase_fast(a):
  n = len(a)
  pref = [0] * (n + 1)
  for i in range(n):
    pref[i + 1] = pref[i] + a[i]

  for i in range(n):
    x = 0
    sign = 1
    for j in range(i, n, 4 * (i + 1)):
      L = j
      R = min(n, j + i + 1)
      x += (pref[R] - pref[L])
    for j in range(i + 2 * (i + 1), n, 4 * (i + 1)):
      L = j
      R = min(n, j + i + 1)
      x -= (pref[R] - pref[L])
    a[i] = int(str(x)[-1])


def process(s, iters):
  s = list(map(int, s))
  for i in range(iters):
    print(i)
    next_phase_fast(s)
  return ''.join(map(str, s))


def main():
  s = input().strip()
  iters = int(sys.argv[1])
  print(process(s, iters)[:8])

  message_offset = int(s[:7])
  print(process(s * 10000, iters)[message_offset:][:8])


if __name__=="__main__":
  main()
