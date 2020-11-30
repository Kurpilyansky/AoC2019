#!/usr/bin/env python3

import sys
from Intcode import *


prog_code = parse_prog_code(sys.argv[1])
program = Program(prog_code)
print(program.run())

