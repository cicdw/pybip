class Knapsack(object):

    def __init__(self, capacity=None):
        self.capacity = capacity
        self.variables = []

    def addVar(self, variable, weight, value):
        self.variables.append(variable)

    def solve(self):
        pass
