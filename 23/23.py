#!/usr/bin/env python3

import time
import os
import sys
import itertools
from queue import Queue
from Intcode import *


class NAT:
  def __init__(self, all_computers):
    self._all_computers = all_computers
    self._memory = None
    
  def has_empty_queue(self):
    return True

  def put_packet(self, x, y):
    print(x, y)
    self._memory = (x, y)

  def process(self):
    if all(map(lambda c: c.has_empty_queue(), self._all_computers.values())):
      print(self._memory)
      self._all_computers[0].put_packet(*self._memory)


class Computer:
  def __init__(self, prog_code, my_address, all_computers):
    self._id = my_address
    self._prog = Program(prog_code, [my_address])
    self._queue = Queue()
    self._all_computers = all_computers

  def has_empty_queue(self):
    return self._queue.empty()

  def put_packet(self, x, y):
    self._queue.put((x, y))

  def process(self):
    if self._queue.empty():
      self._prog.put_input(-1)
    else:
      x, y = self._queue.get()
      self._prog.put_input(x)
      self._prog.put_input(y)
    out = self._prog.run()
    if len(out) % 3 != 0:
      raise ValueError(out)
    for i in range(0, len(out), 3):
      to, x, y = out[i:i+3]
      self._all_computers[to].put_packet(x, y)


prog_code = parse_prog_code(sys.argv[1])

computers = dict()
for i in range(50):
  computers[i] = Computer(prog_code, i, computers)
computers[255] = NAT(computers)

while True:
  for _, c in sorted(computers.items()):
    c.process()

