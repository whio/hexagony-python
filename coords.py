class PointAxial(object):

    def __init__(self, q, r):
        self.q = q
        self.r = r

    def __add__(self, other):
#      if isinstance(other, PointAxial):
        return PointAxial(self.q+other.q, self.r+other.r)

    def __sub__(self, other):
#      if isinstance(other, PointAxial):
        return PointAxial(self.q-other.q, self.r-other.r)

    def to_s():
        return "(%d,%d)" % (self.q, self.r)
