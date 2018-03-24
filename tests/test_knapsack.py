from pybip.problems import Knapsack
from pybip.variables import Var


def test_knapsack_initializes():
    Knapsack()


def test_knapsack_initializes_with_capacity():
    Knapsack(capacity=3)


def test_adding_variables():
    bip = Knapsack(capacity=3)
    bip.add_var(Var(),
               weight=1,
               value=1)


def test_solving_trivial_problem():
    bip = Knapsack(capacity=3)
    bip.add_var(Var(),
               weight=1,
               value=1)
    bip.solve()
    assert bip.variables[0].value == 1


def test_solving_trivial_two_var_problem():
    bip = Knapsack(capacity=3)
    bip.add_var(Var(),
               weight=1,
               value=1)
    bip.add_var(Var(),
               weight=1,
               value=1)
    bip.solve()
    assert all([v.value == 1 for v in bip.variables])


def test_solving_nontrivial_two_var_problem():
    bip = Knapsack(capacity=3)
    bip.add_var(Var(),
               weight=4,
               value=5)
    bip.add_var(Var(),
               weight=1,
               value=1)
    bip.solve()
    assert bip.variables[0].value == 0
    assert bip.variables[1].value == 1


def test_solving_two_var_problem_with_negative_weights():
    bip = Knapsack(capacity=3)
    bip.add_var(Var(),
               weight=-4,
               value=5)
    bip.add_var(Var(),
               weight=1,
               value=1)
    bip.solve()
    assert bip.variables[0].value == 1
    assert bip.variables[1].value == 1


def test_solving_nontrivial_four_var_problem():
    bip = Knapsack(capacity=14)
    bip.add_var(Var(),
               weight=5,
               value=8)
    bip.add_var(Var(),
               weight=7,
               value=11)
    bip.add_var(Var(),
               weight=4,
               value=6)
    bip.add_var(Var(),
               weight=3,
               value=4)
    bip.solve()
    values = [v.value for v in bip.variables]
    assert values == [0, 1, 1, 1]


def test_solving_nontrivial_eight_var_problem():
    bip = Knapsack(capacity=104)
    for weight, value in zip([25, 35, 45, 5, 25, 3, 2, 2],
                             [350, 400, 450, 20, 70, 8, 5, 5]):
        bip.add_var(Var(), weight=weight, value=value)

    bip.solve()
    values = [v.value for v in bip.variables]
    assert values == [1, 0, 1, 1, 1, 0, 1, 1]
