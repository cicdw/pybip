from functools import lru_cache
import numpy as np

from .variables import Var


def _knapsack_table(weights, values, capacity, offset=0):
    """Classic DP solution to the Knapsack problem.  Assumes weights are
    strictly positive integers.

    Returns a table satisfying table[i, j] = max possible value
    of first i items under the weight constraint total(weight) <= j
    """
    n = len(values)
    lookup = np.ones((n + 1, capacity + 1)) * offset

    for item_idx in range(1, n + 1):
        for lim in range(capacity + 1):
            prev_val = lookup[item_idx - 1, lim]
            if weights[item_idx - 1] > lim:
                lookup[item_idx, lim] = prev_val
            else:
                lookup[item_idx, lim] = max(prev_val,
                                            lookup[item_idx - 1, lim - weights[item_idx - 1]] + values[item_idx - 1])

    return lookup


def _knapsack_solution(lookup, weights):
    @lru_cache(maxsize=None)
    def recurse(i, j):
        if i == 0:
            return set()
        if lookup[i, j] > lookup[i - 1, j]:
            return {i}.union(recurse(i - 1, j - weights[i - 1]))
        else:
            return recurse(i - 1, j)
    return recurse(len(weights), lookup.shape[1] - 1)


class Knapsack(object):

    def __init__(self, capacity=None, weights=None, values=None):
        self.capacity = capacity
        self.variables = []
        self.offset = 0
        if ((weights is not None and values is None) or
            (values is not None and weights is None)):
            raise ValueError('Both weights and values must be provided!')

        self.weights = []
        self.values = []
        if weights is not None:
            for weight, value in zip(weights, values):
                self.add_var(Var(), weight, value)

    def add_var(self, variable, weight, value):
        is_pos = weight >= 0
        self.variables.append(variable if is_pos else 1 - variable)
        self.weights.append(weight if is_pos else -weight)
        self.values.append(value if is_pos else -value)
        self.capacity += 0 if is_pos else -weight
        self.offset += 0 if is_pos else value

    def solve(self):
        lookup = _knapsack_table(self.weights,
                                 self.values,
                                 self.capacity,
                                 offset=self.offset)
        sol_idx = _knapsack_solution(lookup, self.weights)
        for idx, var in enumerate(self.variables):
            is_on = (idx + 1) in sol_idx
            var.set_value(1 if is_on else 0)

        self.optimal_value = sum([v * x.value for v, x in zip(self.values, self.variables)]) + self.offset


class EqualityConstrained(object):
    pass


class InequalityConstrained(object):

    def __init__(self, objective=None, constraint=None):
        self.objective = objective
        if constraint.op not in ('le', 'ge'):
            raise ValueError("Current only <= and >= constraints are supported.")
        if constraint.op == 'ge':
            self.constraint = -constraint
        else:
            self.constraint = constraint

    def solve(self):
        bip = Knapsack(capacity = self.constraint.rhs)
        variables = self.constraint.get_variables()
        for var, weight, value in zip(variables, self.constraint.exp.coefs, self.objective.coefs):
            bip.add_var(var, weight, value)
        bip.solve()
        self.optimal_value = bip.optimal_value + self.objective.offset
