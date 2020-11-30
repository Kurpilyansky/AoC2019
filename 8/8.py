#!/usr/bin/env python3

import sys
import numpy as np

def split_chunks(s, x):
  return [s[i:i+x] for i in range(0, len(s), x)]

class ImageLayer:
  def __init__(self, s, w, h):
    self.ps = split_chunks(s, w)

  def count(self, val):
    return sum([s.count(val) for s in self.ps])

  def get_color(self, x, y):
    return self.ps[x][y]

  def __repr__(self):
    return str(self.ps)

class Image:
  def __init__(self, s, w, h):
    print(len(s))
    self.ls = [ImageLayer(x, w, h) for x in split_chunks(s, w * h)]

  def get_color(self, x, y):
    for layer in self.ls:
      val = layer.get_color(x, y)
      if val != '2':
        return val
    return '1'

  def __repr__(self):
    return str(self.ls)

width = int(sys.argv[1])
height = int(sys.argv[2])
image = Image(input().strip(), width, height)
index = np.argmin([layer.count('0') for layer in image.ls])
print(image.ls[index].count('1') * image.ls[index].count('2'))


for y in range(height):
  s = ''
  for x in range(width):
    s += ' ' if image.get_color(y, x) == '0' else '#'
  print(s)
