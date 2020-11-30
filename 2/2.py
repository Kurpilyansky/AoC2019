#!/usr/bin/env python3

import sys

def apply(op, arg1, arg2):
  if op == 1:
    return arg1 + arg2
  elif op == 2:
    return arg1 * arg2
  else:
    raise ValueError('Unexpected op %d' % op)

def run_program(program, v1, v2):
  program[1] = v1
  program[2] = v2

  ip = 0
  while True:
    if program[ip] == 99:
      break
    pos1 = program[ip + 1]
    pos2 = program[ip + 2]
    pos3 = program[ip + 3]
    program[pos3] = apply(program[ip], program[pos1], program[pos2])
    ip += 4
  return program[0]

program = list(map(int, input().split(',')))

print(run_program(list(program), 12, 2))

for i1 in range(100):
  for i2 in range(100):
    try:
      res = run_program(list(program), i1, i2)
      if res == 19690720:
        print(100 * i1 + i2)
    except:
      pass
