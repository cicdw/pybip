import numpy as np


class Var(object):
    __slots__ = ('name', 'value')

    def __init__(self, name=None):
        self.name = name or id(self)
        self.value = None

    def set_value(self, val):
        self.value = val

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
            self.add_term(other, coef=1)
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

    def __lt__(self, other):
        return Constraint(self, 'lt', other)

    def __le__(self, other):
        return Constraint(self, 'le', other)

    def __gt__(self, other):
        return Constraint(self, 'gt', other)

    def __ge__(self, other):
        return Constraint(self, 'ge', other)

    def __eq__(self, other):
        return Constraint(self, 'eq', other)


class Constraint(object):

    def __init__(self, exp, op, rhs):
        if not np.isclose(exp.offset, 0):
            rhs += -exp.offset
            exp.offset = 0
        self.exp = exp
        self.op = op
        self.rhs = rhs

    def get_variables(self):
        return self.exp.terms

    def __neg__(self):
        reverse = {'le': 'ge',
                   'lt': 'gt',
                   'ge': 'le',
                   'gt': 'lt'}
        return Constraint(-self.exp, reverse[self.op], -self.rhs)
