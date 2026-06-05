import re

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[('.',False)] * (size+i) for i in range(size) + range(size-1)[::-1]]

    @staticmethod
    def from_string(string):
        src_dbg = re.sub('\s', '', string)
        src = re.sub('`', '', src_dbg)
        src_len = len(src)

        # Find size of the grid as the smallest regular hexagon which
        # is not smaller than the source code.
        n = 1
        while src_len > 3*n*(n-1) + 1:
            n += 1

        grid_len = 3*n*(n-1) + 1
        src_dbg += '.' * (grid_len - src_len)

        grid = Grid(n)

        debug = False
        ops = []

        for c in src_dbg:
            if c == '`':
                debug = True
            else:
                ops.append((c, debug))
                debug = False

        g = []
        for i in range(n) + range(n-1)[::-1]:
            row_len = n + i
            g.append(ops[:row_len])
            ops = ops[row_len:]
            
        grid.grid = g
        return grid

    def axial_to_index(self, coords):
        x = coords.q
        z = coords.r
        y = -x-z
        if max([abs(x), abs(y), abs(z)]) >= self.size:
            return (None, None)

        i = z + self.size-1
        j = x + min(i, self.size-1)
        return (i, j)

    def get(self, coords):
        i, j = self.axial_to_index(coords)

        if i is not None:
            return self.grid[i][j]
        else:
            return None

    def set(self, coords, value):
        i, j = self.axial_to_index(coords)

        if i is not None:
            self.grid[i][j] = value

    def to_s(self):
        return "\n".join([" "*(2*self.size-1 - len(line)) + "".join([('`' if t[1] else ' ') + t[0] for t in line]) for line in self.grid])
