#!/usr/bin/env python3

import sys

def good_password1(x):
  s = str(x)
  if len(s) != 6:
    return False
  has_double = False
  for i in range(1, len(s)):
    if s[i - 1] > s[i]:
      return False
    if s[i - 1] == s[i]:
      has_double = True
  return has_double

def good_password2(x):
  if not good_password1(x):
    return False
  s = str(x)
  for i in range(10):
    if s.count(chr(i + ord('0'))) == 2:
      return True
  return False

L, R = map(int, input().split('-'))

print(len([x for x in range(L, R + 1) if good_password1(x)]))
print(len([x for x in range(L, R + 1) if good_password2(x)]))
