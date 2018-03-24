from pybip.problems import Knapsack
from pybip.variables import Var


def test_knapsack_initializes():
    Knapsack()


def test_knapsack_initializes_with_capacity():
    Knapsack(capacity=3)


def test_knapsack_initializes_with_everything():
    Knapsack(capacity=3, weights=[1, 2, 3], values=[5, 6, 7])


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
    assert bip.optimal_value == 1


def test_solving_trivial_problem_alt_init():
    bip = Knapsack(capacity=3, weights=[1], values=[1])
    bip.solve()
    assert bip.variables[0].value == 1
    assert bip.optimal_value == 1


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
    assert bip.optimal_value == 2


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
    assert bip.optimal_value == 1


def test_solving_two_var_problem_with_negative_weights():
    bip = Knapsack(capacity=3)
    x, y = Var(), Var()
    bip.add_var(x,
               weight=-4,
               value=5)
    bip.add_var(y,
               weight=1,
               value=1)
    bip.solve()
    assert x.value == 1
    assert y.value == 1
    assert bip.optimal_value == 6


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
    assert bip.optimal_value == 21


def test_solving_nontrivial_eight_var_problem():
    bip = Knapsack(capacity=104)
    for weight, value in zip([25, 35, 45, 5, 25, 3, 2, 2],
                             [350, 400, 450, 20, 70, 8, 5, 5]):
        bip.add_var(Var(), weight=weight, value=value)

    bip.solve()
    values = [v.value for v in bip.variables]
    assert values == [1, 0, 1, 1, 1, 0, 1, 1]
    assert bip.optimal_value == 900


def test_knapsack_with_negative_values():
    bip = Knapsack(capacity=10)
    bip.add_var(Var(), weight=4, value=-2)
    bip.add_var(Var(), weight=20, value=5)
    bip.solve()
    assert [v.value for v in bip.variables] == [0, 0]
    assert bip.optimal_value == 0


def test_knapsack_with_negative_values_neg_weights():
    bip = Knapsack(capacity=10)
    x, y = Var(), Var()
    bip.add_var(x, weight=15, value=-2)
    bip.add_var(y, weight=-5, value=5)
    bip.solve()
    assert [x.value, y.value] == [0, 1]
    assert bip.optimal_value == 5
