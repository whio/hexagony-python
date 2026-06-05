import coords

class NorthEast:
    def reflect_diag_up(self): return NorthEast()
    def reflect_diag_down(self): return West()
    def reflect_hori(self): return SouthEast()
    def reflect_vert(self): return NorthWest()
    def reflect_branch_left(self, cond): return SouthWest()
    def reflect_branch_right(self, cond): return East()

    def vec(self): return coords.PointAxial(1,-1)
    def __eq__(self, other): return isinstance(other, NorthEast)

class NorthWest:
    def reflect_diag_up(self): return East()
    def reflect_diag_down(self): return NorthWest()
    def reflect_hori(self): return SouthWest()
    def reflect_vert(self): return NorthEast()
    def reflect_branch_left(self, cond): return West()
    def reflect_branch_right(self, cond): return SouthEast()

    def vec(self): return coords.PointAxial(0,-1)
    def __eq__(self, other): return isinstance(other, NorthWest)

class West:
    def reflect_diag_up(self): return SouthEast()
    def reflect_diag_down(self): return NorthEast()
    def reflect_hori(self): return West()
    def reflect_vert(self): return East()
    def reflect_branch_left(self, cond): return East()
    def reflect_branch_right(self, cond): return NorthWest() if cond else SouthWest()

    def vec(self): return coords.PointAxial(-1,0)
    def __eq__(self, other): isinstance(other, West)

class SouthWest:
    def reflect_diag_up(self): return SouthWest()
    def reflect_diag_down(self): return East()
    def reflect_hori(self): return NorthWest()
    def reflect_vert(self): return SouthEast()
    def reflect_branch_left(self, cond): return West()
    def reflect_branch_right(self, cond): return NorthEast()

    def vec(self): return coords.PointAxial(-1,1)
    def __eq__(self, other): isinstance(other, SouthWest)

class SouthEast:
    def reflect_diag_up(self): return West()
    def reflect_diag_down(self): return SouthEast()
    def reflect_hori(self): return NorthEast()
    def reflect_vert(self): return SouthWest()
    def reflect_branch_left(self, cond): return NorthWest()
    def reflect_branch_right(self, cond): return East()

    def vec(self): return coords.PointAxial(0,1)
    def __eq__(self, other): isinstance(other, SouthEast)

class East:
    def reflect_diag_up(self): return NorthWest()
    def reflect_diag_down(self): return SouthWest()
    def reflect_hori(self): return East()
    def reflect_vert(self): return West()
    def reflect_branch_left(self, cond): return SouthEast() if cond else NorthEast()
    def reflect_branch_right(self, cond): return West()

    def vec(self): return coords.PointAxial(1,0)
    def __eq__(self, other): isinstance(other, East)
