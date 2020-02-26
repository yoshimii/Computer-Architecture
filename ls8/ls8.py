#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
    
try:
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        cpu = CPU()
        cpu.load(filename)
        cpu.run()
    else: 
        print("Not enough arguments.")
                
except FileNotFoundError:
    print("Filename invalid. Try again with something like: 'examples/mult.ls8'")