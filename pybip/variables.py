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

    def __add__(self, other):
        if self.value is not None:
            return self.value + other
        self.transform = lambda x: x + other
        return self

    def __radd__(self, other):
        if self.value is not None:
            return self.value + other
        self.transform = lambda x: x + other
        return self

    def __mul__(self, other):
        if self.value is not None:
            return self.value * other
        self.transform = lambda x: x / other
        return self

    def __rmul__(self, other):
        if self.value is not None:
            return self.value * other
        self.transform = lambda x: x / other
        return self

    def __rsub__(self, other):
        if self.value is not None:
            return other - self.value
        self.transform = lambda x: other - x
        return self

    def __sub__(self, other):
        if self.value is not None:
            return self.value - other
        self.transform = lambda x: x + other
        return self
