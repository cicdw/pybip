from pybip.problems import InequalityConstrained
from pybip.variables import Var


def test_init_with_kwargs():
    x, y = Var(), Var()
    InequalityConstrained(objective=2 * x + 3 * y,
                          constraint= x + y <= 1)


def test_trivial_solves():
    x, y = Var(), Var()
    bip = InequalityConstrained(objective=2 * x + 3 * y,
                                constraint= x + y <= 1)
    bip.solve()
    assert x.value == 0
    assert y.value == 1

    x, y = Var(), Var()
    bip = InequalityConstrained(objective=2 * x + 3 * y,
                                constraint= x + y >= 1)
    bip.solve()
    assert x.value == 1
    assert y.value == 1
