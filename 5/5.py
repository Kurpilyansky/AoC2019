#!/usr/bin/env python3

import sys

class HaltError(Exception):
  pass


class Argument:
  def __init__(self, prog, addr, mode):
    self._prog = prog
    self._addr = addr
    self._mode = mode

  def pos(self):
    return self._prog.data(self._addr)

  def val(self):
    if self._mode == 0:
      return self._prog.data(self._prog.data(self._addr))
    elif self._mode == 1:
      return self._prog.data(self._addr)
    else:
      raise ValueError("Unexpected mode %d" % self._mode)

  def __repr__(self):
    return '(addr %d mode %d)' % (self._addr, self._mode)
    #return '(addr %d mode %d pos %d val %d)' % (self._addr, self._mode, self.pos(), self.val())

class Program:
  def __init__(self, vals, inputs):
    self.vals = vals
    self.ip = 0
    self.inputs = inputs
    self.outputs = []

  def run(self):
    try:
      while True:
        self._do()
    except HaltError as e:
      print(self.outputs)
      pass

  def data(self, addr):
    try:
      return self.vals[addr]
    except:
      raise ValueError('addr %d is out of range' % addr)


  def _do(self):
    print(self.ip, self.vals[self.ip:][:10])
    op = self.data(self.ip) % 100
    if op == 1:
      self._apply(op, 3, lambda args: self._plus(*args))
    elif op == 2:
      self._apply(op, 3, lambda args: self._multiply(*args))
    elif op == 3:
      self._apply(op, 1, lambda args: self._input(*args))
    elif op == 4:
      self._apply(op, 1, lambda args: self._output(*args))
    elif op == 5:
      self._apply(op, 2, lambda args: self._jmp_if_true(*args))
    elif op == 6:
      self._apply(op, 2, lambda args: self._jmp_if_false(*args))
    elif op == 7:
      self._apply(op, 3, lambda args: self._less_than(*args))
    elif op == 8:
      self._apply(op, 3, lambda args: self._equals(*args))
    elif op == 99:
      raise HaltError()
    else:
      raise ValueError("Unknown op %d" % op)

  def _apply(self, op, args_count, func):
    args = list([Argument(self, self.ip + idx, self.data(self.ip) // (10 ** (1 + idx)) % 10) for idx in range(1, args_count + 1)])
    print(self.ip, op, args)
    if func(args) is None:
      self.ip += args_count + 1

  def _plus(self, arg1, arg2, index):
    self.vals[index.pos()] = arg1.val() + arg2.val()

  def _multiply(self, arg1, arg2, index):
    self.vals[index.pos()] = arg1.val() * arg2.val()

  def _input(self, index):
    if self.inputs:
      self.vals[index.pos()] = self.inputs[0]
      self.inputs = self.inputs[1:]
    else:
      self.vals[index.pos()] = int(input())
  
  def _output(self, val):
    self.outputs.append(val.val())

  def _jmp_if_true(self, val, addr):
    if val.val() != 0:
      self.ip = addr.val()
      return True

  def _jmp_if_false(self, val, addr):
    if val.val() == 0:
      self.ip = addr.val()
      return True

  def _less_than(self, arg1, arg2, index):
    self.vals[index.pos()] = 1 if arg1.val() < arg2.val() else 0

  def _equals(self, arg1, arg2, index):
    self.vals[index.pos()] = 1 if arg1.val() == arg2.val() else 0

with open(sys.argv[1]) as f:
  line = f.readline().strip()
  prog_code = list(map(int, line.split(',')))
program = Program(prog_code, [])

program.run()

