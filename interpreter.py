#!/usr/bin/python

from hexagony import Hexagony
from grid import Grid
import sys

debug_level = 0

if __name__ == "__main__":
    args = sys.argv[1:]
    while args:
        option = args.pop(0)
        if option == "-d":
            debug_level = 1
        elif option == "-D":
            debug_level = 2
        elif option == "-g":
            if args:
                size = int(args.pop(0))
                print(Grid(size).to_s())
            else:
                print("Error: No size given for -g")
            exit(0)
        else:
            source_file = option

    if source_file:
        with open(source_file) as f:
            data = f.read()
            Hexagony(data, debug_level).run()
    else:
        print("Error: missing source!")
