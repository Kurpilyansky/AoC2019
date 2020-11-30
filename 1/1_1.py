#!/usr/bin/env python3

import sys

def get_fuel(x):
  return x // 3 - 2

print(sum(map(get_fuel, map(int, sys.stdin))))
