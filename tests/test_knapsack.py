from pybip.problems import Knapsack
from pybip.variables import Var


def test_knapsack_initializes():
    Knapsack()


def test_knapsack_initializes_with_capacity():
    Knapsack(capacity=3)


def test_adding_variables():
    bip = Knapsack(capacity=3)
    bip.addVar(Var(),
               weight=1,
               value=1)


def test_solving_trivial_problem():
    bip = Knapsack(capacity=3)
    bip.addVar(Var(),
               weight=1,
               value=1)
    bip.solve()
    assert bip.variables[0].value == 1


def test_solving_trivial_two_var_problem():
    bip = Knapsack(capacity=3)
    bip.addVar(Var(),
               weight=1,
               value=1)
    bip.addVar(Var(),
               weight=1,
               value=1)
    bip.solve()
    assert all([v.value == 1 for v in bip.variables])


def test_solving_nontrivial_two_var_problem():
    bip = Knapsack(capacity=3)
    bip.addVar(Var(),
               weight=4,
               value=5)
    bip.addVar(Var(),
               weight=1,
               value=1)
    bip.solve()
    assert bip.variables[0].value == 0
    assert bip.variables[1].value == 1
