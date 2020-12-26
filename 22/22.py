#!/usr/bin/env python3

import time
import os
import sys
import itertools
from queue import Queue


def parse():
  n = int(sys.argv[1])
  val = int(sys.argv[2])
  times = int(sys.argv[3])
  commands = sys.stdin.read().strip('\n').split('\n')
  return n, val, times, commands

def cut(n, index, k):
  k %= n
  if index >= k:
    return index - k
  else:
    return index + n - k

def deal_into_new_deck(n, index):
  return n - index - 1

def deal_with_increment(n, index, k):
  return (index * k) % n

def apply_commands(commands, n, index):
  for command in commands:
    tokens = command.split()
    if tokens[0] == 'cut':
      index = cut(n, index, int(tokens[-1]))
    elif tokens[1] == 'with':
      index = deal_with_increment(n, index, int(tokens[-1]))
    elif tokens[1] == 'into':
      index = deal_into_new_deck(n, index)
    else:
      raise ValueError(command)
  return index


def multiply(A, B, MOD):
  n = len(A)
  C = [[0] * n for i in range(n)]
  for i in range(n):
    for j in range(n):
      for k in range(n):
        C[i][k] += A[i][j] * B[j][k]
        C[i][k] %= MOD
  return C

def power(A, k, MOD):
  n = len(A)
  B = [[0] * n for i in range(n)]
  for i in range(n):
    B[i][i] = 1
  while k != 0:
    if k % 2 == 1:
      B = multiply(A, B, MOD)
    A = multiply(A, A, MOD)
    k //= 2
  return B

def mod_inverse(a, MOD):
  k = MOD - 2
  b = 1
  while k != 0:
    if k % 2 == 1:
      b = (a * b) % MOD
    a = (a * a) % MOD
    k //= 2
  return b

n, index, times, commands = parse()
print(n, index, times)
zero = apply_commands(commands, n, 0)
one = apply_commands(commands, n, 1)

A = [[1, zero], [0, (one - zero) % n]]
A = power(A, times, n)
print((A[0][1] + A[1][1] * index) % n)
print((index - A[0][1]) * mod_inverse(A[1][1], n) % n)
