import operator as oper
import pytest
from pybip.variables import Var


def test_var_initializes_with_name():
    x = Var('x')
    assert x.name == 'x'


def test_var_has_value():
    x = Var()
    assert x.value == None


def test_var_set_value():
    x = Var()
    x.set_value(1)
    assert x.value == 1


def test_derived_var_value_cascade_right():
    x = Var('x')
    y = x - 1
    y.set_value(1)
    assert x.value == 2


def test_derived_var_value_cascade_left():
    x = Var('x')
    y = 1 - x
    y.set_value(1)
    assert x.value == 0


def test_subtraction_after_value_isset():
    x = Var()
    x.set_value(2)
    assert 1 - x == -1
    assert x - 1 == 1


def test_multiplication_after_value_isset():
    x = Var()
    x.set_value(1)
    assert x * 5 == 5
    assert 2 * x == 2


def test_addition_after_value_isset():
    x = Var()
    x.set_value(0)
    assert 3 + x == 3
    assert x + 3 == 3


def test_multiplication_and_subtraction_together():
    x = Var()
    y = 1 - x
    y.set_value(1)
    assert 3 * y == 3


def test_downstream_variable_setting():
    x = Var()
    y = 5 - 2 * x
    z = y + 4
    z.set_value(10)
    assert z.value == 10
    assert y.value == 6
    assert x.value == -0.5


def test_get_ancestors():
    x = Var()
    y = 5 - 2 * x
    z = y + 4
    family = z.get_ancestors()
    assert y in family
    assert x in family


@pytest.mark.parametrize("op", [oper.le, oper.lt, oper.ge, oper.gt, oper.eq],
                         ids=['le', 'lt', 'ge', 'gt', 'eq'])
def test_constraint_ancestors(op):
    x, y = Var(), Var()
    constr = op(x + y, 1)
    variables = constr.get_ancestors()
    assert y in variables
    assert x in variables
