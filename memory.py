# Memory is a pointy-topped hexagonal grid which contains one integer value for
# each edge. That is, the data structure is the line graph of an infinite
# hexagonal grid. Edges are indexed by the axial coordinates of the (westward)
# adjacent hexagon, and a symbol :NE, :E, :SE indicating which of the three
# edges is meant (where the direction is taken from the hexagon to the edge).
# The memory pointer includes another flag which indicates whether the MP
# is currently pointing in the clockwise or counter-clockwise directoin (in
# relation to the hexagon used for indexing).
class Memory:
    def __init__(self):
        self.memory = {}
        self.mp = (0, 0, 1)
        self.cw = False

    #    / \     /
    #  2/  0\  2/
    #\ /     \ /
    # |  q0   |  q1
    # |      1|
    # |  r0   |  r0
    #/ \     / \
    #  0\  2/  0\
    #    \ /     \
    #q-1  |  q0   |
    #    1|      1|
    #r 1  |  r1   |
    #    / \     /
    #  2/   \  2/
    #  /     \ /
    def left_index(self):
        q, r, e = self.mp
        cw = self.cw
        if e == 0:
            if cw:
                return (q+1, r-1, 2), False
            else:
                return (q,   r-1, 2), True
        elif e == 1:
            if cw:
                return (q,   r+1, 0), True
            else:
                return (q,   r,   0), False
        elif e == 2:
            if cw:
                return (q-1, r+1, 1), True
            else:
                return (q,   r,   1), False

    def right_index(self):
        q, r, e = self.mp
        cw = self.cw
        if e == 0:
            if cw:
                return (q,   r,   1), True
            else:
                return (q,   r-1, 1), False
        elif e == 1:
            if cw:
                return (q,   r,   2), True
            else:
                return (q+1, r-1, 2), False
        elif e == 2:
            if cw:
                return (q-1, r+1, 0), False
            else:
                return (q,   r+1, 0), True

    def reverse(self):
        self.cw = not self.cw

    def move_left(self):
        self.mp, self.cw = self.left_index()

    def move_right(self):
        self.mp, self.cw = self.right_index()

    def set(self, value):
        self.memory[self.mp] = value

    def get(self):
        if self.mp not in self.memory:
            self.memory[self.mp] = 0
        return self.memory[self.mp]

    def get_left(self):
        left_mp, _ = self.left_index()
        if left_mp not in self.memory:
            self.memory[left_mp] = 0
        return self.memory[left_mp]

    def get_right(self):
        right_mp, _ = self.right_index()
        if right_mp not in self.memory:
            self.memory[right_mp] = 0
        return self.memory[right_mp]

