#!/usr/bin/env python3

import sys
import itertools
from Intcode import *


prog_code = parse_prog_code(sys.argv[1])

res = 0
for perm in list(itertools.permutations(range(5))):
  cur = 0
  for i in perm:
    program = Program(prog_code, [i, cur])
    cur = program.run()[0]
  res = max(res, cur)
print(res)

res = 0
for perm in list(itertools.permutations(range(5, 10))):
  progs = list([Program(prog_code, [i]) for i in perm])
  cur = 0
  last = 0
  ended = False
  while not ended:
    for prog in progs:
      prog.inputs.append(cur)
      out = prog.run()
      if not out:
        ended = True
        break
      cur = out[0]
    last = cur
  res = max(res, last)
print(res)

