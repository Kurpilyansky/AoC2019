#!/usr/bin/env python3

import sys

def get_fuel(x):
  return x // 3 - 2


def get_total_fuel(x):
  total = 0
  x = get_fuel(x)
  while x >= 0:
    total += x
    x = get_fuel(x)
  return total

print(sum(map(get_total_fuel, map(int, sys.stdin))))
