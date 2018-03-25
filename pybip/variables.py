class Var(object):
    __slots__ = ('name', 'parent', 'value')

    def __init__(self, name=None, parent=None):
        self.name = name or id(self)
        self.value = None
        self.parent = parent

    def set_value(self, val):
        if self.parent is not None:
            v, transform = self.parent
            v.set_value(transform(val))

        self.value = val

    def get_ancestors(self):
        if self.parent is not None:
            parent = self.parent[0]
            return [parent] + parent.get_ancestors()
        else:
            return []

    def __add__(self, other):
        if self.value is not None:
            return self.value + other
        transform = lambda x: x - other
        return Var(parent=(self, transform))

    def __radd__(self, other):
        if self.value is not None:
            return self.value + other
        transform = lambda x: x - other
        return Var(parent=(self, transform))

    def __mul__(self, other):
        if self.value is not None:
            return self.value * other
        transform = lambda x: x / other
        return Var(parent=(self, transform))

    def __rmul__(self, other):
        if self.value is not None:
            return self.value * other
        transform = lambda x: x / other
        return Var(parent=(self, transform))

    def __rsub__(self, other):
        if self.value is not None:
            return other - self.value
        transform = lambda x: other - x
        return Var(parent=(self, transform))

    def __sub__(self, other):
        if self.value is not None:
            return self.value - other
        transform = lambda x: x + other
        return Var(parent=(self, transform))
