from functools import lru_cache
import numpy as np


def _knapsack_table(weights, values, capacity):
    """Classic DP solution to the Knapsack problem.  Assumes weights are
    strictly positive integers.

    Returns a table satisfying table[i, j] = max possible value
    of first i items under the weight constraint total(weight) <= j
    """
    n = len(values)
    lookup = np.zeros((n + 1, capacity + 1))

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

    def __init__(self, capacity=None):
        self.capacity = capacity
        self.variables = []
        self.weights = []
        self.values = []

    def add_var(self, variable, weight, value):
        self.variables.append(variable if weight >= 0 else 1 - variable)
        self.weights.append(weight if weight >= 0 else -weight)
        self.values.append(value)

    def solve(self):
        lookup = _knapsack_table(self.weights,
                                  self.values,
                                  self.capacity)
        sol_idx = _knapsack_solution(lookup, self.weights)
        for idx, var in enumerate(self.variables):
            is_on = (idx + 1) in sol_idx
            var.set_value(1 if is_on else 0)

        self.optimal_value = sum([v * x for v, x in zip(self.values, self.variables)])
