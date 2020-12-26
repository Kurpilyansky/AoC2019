#!/usr/bin/env python3

import sys

class HaltError(Exception):
  pass


class NoInputException(Exception):
  pass


class Argument:
  def __init__(self, prog, addr, mode):
    self._prog = prog
    self._addr = addr
    self._mode = mode

  def pos(self):
    if self._mode == 0:
      return self._prog.data(self._addr)
    elif self._mode == 2:
      return self._prog.data(self._addr) + self._prog.rel_base()
    else:
      raise ValueError("Unexpected mode %d" % self._mode)

  def val(self):
    if self._mode == 0:
      return self._prog.data(self._prog.data(self._addr))
    elif self._mode == 1:
      return self._prog.data(self._addr)
    elif self._mode == 2:
      return self._prog.data(self._prog.data(self._addr) + self._prog.rel_base())
    else:
      raise ValueError("Unexpected mode %d" % self._mode)

  def __repr__(self):
    return '(addr %d mode %d)' % (self._addr, self._mode)
    #return '(addr %d mode %d pos %d val %d)' % (self._addr, self._mode, self.pos(), self.val())

class Program:
  def __init__(self, data, inputs=None, verbose=False):
    self._data = dict({i: data[i] for i in range(len(data))})
    self.ip = 0
    self.inputs = inputs
    self.outputs = []
    self._rel_base = 0
    self._verbose = verbose
    self._is_halted = False

  def is_halted(self):
    return self._is_halted

  def put_input(self, val):
    self.inputs.append(val)

  def put_inputs(self, vals):
    for val in vals:
      self.inputs.append(val)

  def run(self):
    try:
      while True:
        self._do()
    except HaltError as e:
      res = self.outputs
      self.outputs = []
      self._is_halted = True
      return res
    except NoInputException as e:
      res = self.outputs
      self.outputs = []
      return res

  def data(self, addr):
    if addr < 0:
      raise ValueError('addr %d' % addr)
    return self._data.get(addr, 0)

  def write_data(self, addr, value):
    if addr < 0:
      raise ValueError('addr %d' % addr)
    self._data[addr] = value

  def rel_base(self):
    return self._rel_base

  def _do(self):
    if self._verbose:
      print(self.ip, self.rel_base(), [self.data(self.ip + i) for i in range(5)])
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
    elif op == 9:
      self._apply(op, 1, lambda args: self._adjust_rel_base(*args))
    elif op == 99:
      raise HaltError()
    else:
      raise ValueError("Unknown op %d" % op)

  def _apply(self, op, args_count, func):
    args = list([Argument(self, self.ip + idx, self.data(self.ip) // (10 ** (1 + idx)) % 10) for idx in range(1, args_count + 1)])
    if self._verbose:
      print(self.ip, op, args)
    if func(args) is None:
      self.ip += args_count + 1

  def _plus(self, arg1, arg2, index):
    self.write_data(index.pos(), arg1.val() + arg2.val())

  def _multiply(self, arg1, arg2, index):
    self.write_data(index.pos(), arg1.val() * arg2.val())

  def _input(self, index):
    if self.inputs is None:
      self.write_data(index.pos(), int(input()))
    else:
      if self.inputs:
        self.write_data(index.pos(), self.inputs[0])
        self.inputs = self.inputs[1:]
      else:
        raise NoInputException()
  
  def _output(self, val):
    self.outputs.append(val.val())
    if self._verbose:
      print('output %d' % self.outputs[-1])

  def _jmp_if_true(self, val, addr):
    if val.val() != 0:
      self.ip = addr.val()
      return True

  def _jmp_if_false(self, val, addr):
    if val.val() == 0:
      self.ip = addr.val()
      return True

  def _less_than(self, arg1, arg2, index):
    self.write_data(index.pos(), 1 if arg1.val() < arg2.val() else 0)

  def _equals(self, arg1, arg2, index):
    self.write_data(index.pos(), 1 if arg1.val() == arg2.val() else 0)

  def _adjust_rel_base(self, arg):
    self._rel_base += arg.val()


def parse_prog_code(filename):
  with open(sys.argv[1]) as f:
    line = f.readline().strip()
    return list(map(int, line.split(',')))


