#!/usr/bin/env python3

import time
import os
import sys
import itertools
import re
from Intcode import *

def decode(ints):
  def dec(i):
    if i < 256:
      return chr(i)
    else:
      return str(i)

  return ''.join(map(dec, ints))


def encode(s):
  return list(map(ord, s))


def parse_description(descr):
  descr = decode(descr).strip()
  #print(descr)
  blocks = descr.split('\n\n')
  res = dict()
  for block in blocks:
    block = block.strip()
    if block.startswith('=='):
      name, text = block.split('\n')
      res["location"] = {"name": name.strip('=').strip(),
                         "text": text}
    elif block.startswith('Doors here lead:'):
      res["doors"] = list(map(lambda s: s.strip('- '), block.split('\n')[1:]))
    elif block.startswith('Items here:'):
      res["items"] = list(map(lambda s: s.strip('- '), block.split('\n')[1:]))
    elif block.startswith('Command?'):
      pass
    else:
      print('Unknown block: "%s"' % block)
  #print(res)
  return res


banned_items = {'infinite loop', 'molten lava', 'giant electromagnet', 'escape pod', 'photons'}
directions = ['north', 'east', 'south', 'west']

class Droid:
  def __init__(self, prog_code):
    self._prog = Program(prog_code, [])
    self._state = {}
    self._visited = set()
    self._dir = 1
    self._inventory = set()

  def _update_state(self):
    out = self._prog.run()
    descr = parse_description(out)
    self._state.update(descr)

  def _visit(self):
    if self._state["location"]["name"] not in self._visited:
      self._visited.add(self._state["location"]["name"])
      print()
      print(self._state["location"]["name"])
      print(self._state["location"]["text"])

    for item in self._state.get('items', []):
      if item not in banned_items:
        print('Getting %s' % item)
        self._prog.put_inputs(encode('take %s\n' % item))
        out = self._prog.run()
        print(decode(out).strip())
        self._inventory.add(item)
    self._state['items'] = []
   


  def _go(self):
    for i in range(1, -3, -1):
      new_dir = (self._dir + i) % 4
      if directions[new_dir] in self._state['doors']:
        print('Going to %s' % directions[new_dir])
        self._dir = new_dir
        self._prog.put_inputs(encode(directions[new_dir] + '\n'))
        return
        

  def _manual(self):
    allowed_commands = []
    for door in self._state.get('doors', []):
      allowed_commands.append(door)
    for item in self._state.get('items', []):
      allowed_commands.append('take %s' % item)

    for i, command in enumerate(allowed_commands):
      print(i, '-', command)
    
    inp = input()
    try:
      inp = allowed_commands[int(inp)]
    except:
      pass

    command = encode(inp + '\n')
    print(command)
    self._prog.put_inputs(command)

  def run(self):
    while True:
      self._update_state()
      self._visit()
      self._go()

      if False and self._state['location']['name'] == 'Navigation':
        self._prog.put_inputs(encode('529920\n'))
        out = self._prog.run()
        print(decode(out))
    
      if self._state['location']['name'] == 'Security Checkpoint':
        print('Have %d items: %s' % (len(self._inventory), ', '.join(self._inventory)))
        if len(self._inventory) == 8:
          break

    all_items = list(self._inventory)
    for mask in range(1, (1 << len(all_items))):
      for i, item in enumerate(all_items):
        if (mask & (1 << i)):
          if item not in self._inventory:
            self._inventory.add(item)
            self._prog.put_inputs(encode('take %s\n' % item))
            self._prog.run()
        else:
          if all_items[i] in self._inventory:
            self._inventory.remove(item)
            self._prog.put_inputs(encode('drop %s\n' % item))
            self._prog.run()

      self._prog.put_inputs(encode('north\n'))
      out = self._prog.run()
      print(decode(out))
    

prog_code = parse_prog_code(sys.argv[1])
droid = Droid(prog_code)
droid.run()

