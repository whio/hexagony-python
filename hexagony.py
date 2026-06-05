import sys
from grid import Grid
from memory import Memory
from coords import PointAxial
#from direction import East, West, NorthEast, NorthWest, SouthEast, SouthWest
from direction import *

class Hexagony:

    def __init__(self, src, debug_level=0, in_str=sys.stdin, out_str=sys.stdout, max_ticks=-1):
        self.debug_level = debug_level
        self.in_str = in_str
        self.out_str = out_str
        self.max_ticks = max_ticks
        self.debug_tick = False
        self.grid = Grid.from_string(src)
        self.tick = 0
        self.next_byte = None

        self.memory = Memory()

        n = self.grid.size-1
        self.ips = [                                    #    ______            ______
            [PointAxial( 0, -n), East()],               #   /0,-n  \          /  n,-n\
            [PointAxial( n, -n), SouthEast()],          #  /  \     \        /        \
            [PointAxial( n,  0), SouthWest()],          # /    \ q   \      /   ____   \
            [PointAxial( 0,  n), West()],               # \-n,0 \    /      \    r  n,0/
            [PointAxial(-n,  n), NorthWest()],          #  \     \  /        \        /
            [PointAxial(-n,  0), NorthEast()]           #   \______/0,n   -n,n\______/
        ]
        self.active_ip = self.new_ip = 0

    def dir(self):
        return self.ips[self.active_ip][1]

    def coords(self):
        return self.ips[self.active_ip][0]

    def run(self):
        if self.grid.size < 1:
            return

        while (self.max_ticks < 0 or self.tick < self.max_ticks):

            cmd, dbg = self.grid.get(self.coords())
            self.debug_tick = self.debug_level > 1 or (self.debug_level > 0 and dbg)
            if self.debug_tick:
                sys.stderr.write("\nTick #{0}:\n".format(self.tick))
                sys.stderr.write("IPs (! indicates active IP):\n")
                for i, ip in enumerate(self.ips):
                    sys.stderr.write("{0} {1} {2} {3}\n".format('!' if i == self.active_ip else ' ', i, ip[0], ip[1]))
                sys.stderr.write("Command: {0} Debug: {1}\n".format(repr(cmd), dbg))
            if cmd == '@':
                if self.debug_tick:
                    sys.stderr.write("Memory: {0}\n".format(repr(memory)))
                break

            self.process(cmd)
            if self.debug_tick:
                sys.stderr.write("New direction: {0}\n".format(repr(dir)))
                sys.stderr.write("Memory: {0}\n".format(repr(self.memory)))
            self.ips[self.active_ip][0] += self.dir().vec()

            self.handle_edges()
            self.active_ip = self.new_ip
            self.tick += 1

        return self.max_ticks > -1 and self.tick >= self.max_ticks

    def process(self, cmd):
        opcode = cmd

        # Arithmetic
        if opcode >= '0' and opcode <= '9':
            val = self.memory.get()
            if val < 0:
                self.memory.set(val*10 - int(opcode))
            else:
                self.memory.set(val*10 + int(opcode))
        elif opcode == ')':
            self.memory.set(self.memory.get()+1)
        elif opcode == '(':
            self.memory.set(self.memory.get()-1)
        elif opcode == '+':
            self.memory.set(self.memory.get_left() + self.memory.get_right())
        elif opcode == '-':
            self.memory.set(self.memory.get_left() - self.memory.get_right())
        elif opcode == '*':
            self.memory.set(self.memory.get_left() * self.memory.get_right())
        elif opcode == ':':
            self.memory.set(self.memory.get_left() / self.memory.get_right())
        elif opcode == '%':
            self.memory.set(self.memory.get_left() % self.memory.get_right())
        elif opcode == '~':
            self.memory.set(-self.memory.get())

        # Memory manipulation
        elif opcode == '{':
            self.memory.move_left()
        elif opcode == '}':
            self.memory.move_right()
        elif opcode == '=':
            self.memory.reverse()
        elif opcode == '"':
            self.memory.reverse()
            self.memory.move_right()
            self.memory.reverse()
        elif opcode == '\'':
            self.memory.reverse()
            self.memory.move_left()
            self.memory.reverse()
        elif opcode == '^':
            if self.memory.get() > 0:
                self.memory.move_right()
            else:
                self.memory.move_left()
        elif opcode == '&':
            if self.memory.get() > 0:
                self.memory.set(self.memory.get_right())
            else:
                self.memory.set(self.memory.get_left())
        elif (opcode >= 'A' and opcode <= 'Z') or (opcode >= 'a' and opcode <= 'z'):
            self.memory.set(ord(opcode))

        # I/O
        elif opcode == ',':
            byte = self.read_byte()
            self.memory.set(ord(byte) if byte is not None else -1)
        elif opcode == ';':
            self.out_str.write(chr(self.memory.get() % 256))
        elif opcode == '?':
            val = 0
            sign = 1
            while(True):
                byte = self.read_byte()
                if byte == '+':
                    sign = 1
                elif byte == '-':
                    sign = -1
                elif (byte >= '0' and byte <= '9') or byte is None:
                    self.next_byte = byte
                else:
                    continue
                break

            while(True):
                byte = self.read_byte()
                if byte is not None and (byte >= '0' and byte <= '9'):
                    val = val*10 + int(byte)
                else:
                    self.next_byte = byte
                    break

            self.memory.set(sign*val)
        elif opcode == '!':
            self.out_str.write(str(self.memory.get()))

        # Control flow
        elif opcode == '$':
            self.ips[self.active_ip][0] += self.dir().vec()
            self.handle_edges()
        elif opcode == '_':
            self.ips[self.active_ip][1] = self.dir().reflect_hori()
        elif opcode == '|':
            self.ips[self.active_ip][1] = self.dir().reflect_vert()
        elif opcode == '/':
            self.ips[self.active_ip][1] = self.dir().reflect_diag_up()
        elif opcode == '\\':
            self.ips[self.active_ip][1] = self.dir().reflect_diag_down()
        elif opcode == '<':
            self.ips[self.active_ip][1] = self.dir().reflect_branch_left(self.memory.get() > 0)
        elif opcode == '>':
            self.ips[self.active_ip][1] = self.dir().reflect_branch_right(self.memory.get() > 0)
        elif opcode == ']':
            self.new_ip = (self.active_ip+1) % 6
        elif opcode == '[':
            self.new_ip = (self.active_ip-1) % 6
        elif opcode == '#':
            self.new_ip = self.memory.get % 6

        # Others
        elif opcode == '@':
            raise Exception('[BUG] Received :terminate. This shouldn\'t happen.')
        elif opcode == '.':
            None  # Nop

    def handle_edges(self):
        x = self.coords().q
        z = self.coords().r
        y = -x-z

        extents = [abs(x), abs(y), abs(z)]

        if self.grid.size == 1:
            self.ips[self.active_ip][0] = PointAxial.new(0,0)
        elif max(extents) >= self.grid.size:
            # First, determine pivot: if there's only one value at @size, that's the pivot.
            # If there's two, if @memory.get > 0, the pivot is the first coordinate in a
            # cyclically adjacent pair. Otherwise it's the second one.
            # Now undo the last step.
            # Finally, to do the wrapping, negate all three values and swap the non-pivot values.
            max_indices = [i for i, e in enumerate(extents) if abs(e) >= self.grid.size]

            if len(max_indices) == 1:
                pivot = max_indices[0]
            elif len(max_indices) == 2:
                a, b = max_indices
                # We want the first index, if we consider the two as a cyclically adjacent pair.
                # i.e.
                # a b  pivot
                # 0 1  0
                # 1 2  1
                # 2 0  2
                # 1 0  0
                # 2 1  1
                # 0 2  2
                pivot = b if (a-b)%3 == 1 else a
                # Pick the other one if current cell is non-positive
                if self.memory.get() <= 0:
                    pivot = (pivot+1)%3

            i, j = [k for k in range(3) if k != pivot]

            self.ips[self.active_ip][0] -= self.dir().vec()

            x = self.coords().q
            z = self.coords().r
            y = -x-z

            wrapped = [-x, -y, -z]
            wrapped[i], wrapped[j] = wrapped[j], wrapped[i]

            x, _, z = wrapped

            self.ips[self.active_ip][0].q = x
            self.ips[self.active_ip][0].r = z

    def read_byte(self):
        result = None
        if self.next_byte is not None:
            result = self.next_byte
            self.next_byte = None
        else:
            result = self.in_str.read(1)
        return result

