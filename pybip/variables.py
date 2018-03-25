class VariableContainer(object):
    __slots__ = ('name', 'parents')

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


class Var(VariableContainer):
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

    def _handle_other(self, other, transform):
        parents = [(self, transform)]
        if isinstance(other, Var):
            parents.append((other, transform))
        return Var(parents=parents)

    def __add__(self, other):
        if isinstance(other, LinearExpression):
            other.add_term(self, coef=1)
            return other
        else:
            return LinearExpression(terms=self, coefs=[1], offset=other)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Multiplication with Variables is only support for int and float.")
        else:
            return LinearExpression(terms=self, coefs=[other], offset=0)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        if isinstance(other, LinearExpression):
            other.add_term(self, coef=-1)
            return -other
        else:
            return LinearExpression(terms=self, coefs=[1], offset=-other)

    def __rsub__(self, other):
        if isinstance(other, LinearExpression):
            other.add_term(self, coef=-1)
            return other
        else:
            return LinearExpression(terms=self, coefs=[-1], offset=other)


class LinearExpression(object):
    def __init__(self, terms, coefs, offset):
        if not isinstance(terms, list):
            terms = [terms]
        self.terms = terms
        self.coefs = coefs
        self.offset = offset

    def add_term(self, term, coef=1):
        if term in self.terms:
            self.coefs[self.terms.index(term)] += coef
        else:
            self.terms.append(term)
            self.coefs.append(coef)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, other):
        if isinstance(other, Var):
            self.add_term(Var, coef=1)
            self._offset = 0
        else:
            self._offset = other

    @property
    def value(self):
        res = self.offset
        for coef, term in zip(self.coefs, self.terms):
            res += coef * term.value
        return res

    def set_value(self, value):
        if len(self.terms) > 1:
            raise ValueError("Cannot set value on Linear Expression containing multiple variables.")

        x, a, b = self.terms[0], self.coefs[0], self.offset
        x.set_value((value - b) / a)

    def __add__(self, other):
        if isinstance(other, LinearExpression):
            for term, coef in zip(other.terms, other.coefs):
                self.add_term(term, coef=coef)
            self.offset = self.offset + other.offset
        elif isinstance(other, Var):
            self.add_term(other, coef=1)
        else:
            self.offset = self.offset + other
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Multiplication with Variables is only support for int and float.")
        else:
            self.coefs = [other * coef for coef in self.coefs]
            self.offset = other * self.offset
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return -self.__add__(-other)

    def __neg__(self):
        self.coefs = [-c for c in self.coefs]
        self.offset = -self.offset
        return self


class Constraint(VariableContainer):

    def __init__(self, exp, op, rhs):
        self.parents = [(exp,)]
        self.exp = exp
        self.op = op
        self.rhs = rhs
