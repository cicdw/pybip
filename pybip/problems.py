from functools import lru_cache
import numpy as np


def _knapsack_table(weights, values, capacity):
    """Classic DP solution to the Knapsack problem.  Assumes weights are
    strictly positive integers.
    """
    n = len(values)
    lookup = np.zeros((n + 1, capacity))
    for i in range(1, n + 1):
        for j in range(capacity):
            prev_val = lookup[i - 1, j]
            if weights[i - 1] > j:
                lookup[i, j] = prev_val
            else:
                lookup[i, j] = max(prev_val, lookup[i - 1, j - weights[i - 1]] + values[i - 1])
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

    def __init__(self, capacity=None):
        self.capacity = capacity
        self.variables = []
        self.weights = []
        self.values = []

    def addVar(self, variable, weight, value):
        self.variables.append(variable)
        self.weights.append(weight)
        self.values.append(value)

    def solve(self):
        lookup = _knapsack_table(self.weights,
                                  self.values,
                                  self.capacity)
        sol_idx = _knapsack_solution(lookup, self.weights)
        for idx, var in enumerate(self.variables):
            var.set_value(1 if (idx + 1) in sol_idx else 0)
