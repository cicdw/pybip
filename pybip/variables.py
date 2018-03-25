class Var(object):
    __slots__ = ('name', 'parents', 'value')

    def __init__(self, name=None, parents=None):
        self.name = name or id(self)
        self.value = None
        self.parents = parents

    def set_value(self, val):
        if self.parents is not None:
            for parent in self.parents:
                v, transform = parent
                v.set_value(transform(val))

        self.value = val

    def get_ancestors(self):
        if self.parents is not None:
            out = []
            for parent in self.parents:
                var = parent[0]
                out.append(var)
                out.extend(var.get_ancestors())
            return out
        else:
            return []

    def _handle_other(self, other, transform):
        parents = [(self, transform)]
        if isinstance(other, Var):
            parents.append((other, transform))
        return Var(parents=parents)

    def __add__(self, other):
        if self.value is not None:
            return self.value + other
        transform = lambda x: x - other
        return self._handle_other(other, transform)

    def __radd__(self, other):
        if self.value is not None:
            return self.value + other
        transform = lambda x: x - other
        return self._handle_other(other, transform)

    def __mul__(self, other):
        if self.value is not None:
            return self.value * other
        transform = lambda x: x / other
        return self._handle_other(other, transform)

    def __rmul__(self, other):
        if self.value is not None:
            return self.value * other
        transform = lambda x: x / other
        return self._handle_other(other, transform)

    def __rsub__(self, other):
        if self.value is not None:
            return other - self.value
        transform = lambda x: other - x
        return self._handle_other(other, transform)

    def __sub__(self, other):
        if self.value is not None:
            return self.value - other
        transform = lambda x: x + other
        return self._handle_other(other, transform)

    def __le__(self, other):
        return Constraint(self, op='leq', rhs=other)


class Constraint(Var):

    def __init__(self, exp, op, rhs):
        super().__init__(self, parents=[(exp,)])
        self.exp = exp
        self.op = op
        self.rhs = rhs
