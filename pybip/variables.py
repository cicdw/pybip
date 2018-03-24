class Var(object):
    __slots__ = ('name', 'transform', 'value')

    def __init__(self, name=None):
        self.name = name or id(self)
        self.value = None

    def set_value(self, val):
        if hasattr(self, 'transform'):
            self.value = self.transform(val)
        else:
            self.value = val

    def __rsub__(self, other):
        self.transform = lambda x: other - x
        return self

    def __sub__(self, other):
        self.transform = lambda x: x + other
        return self
