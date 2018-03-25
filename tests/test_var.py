import numpy as np
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


def test_downstream_variable_setting():
    x = Var()
    y = 5 - 2 * x
    z = y + 4
    z.set_value(10)
    np.testing.assert_almost_equal(x.value, -0.5)


def test_get_terms():
    x = Var()
    y = 5 - 2 * x
    z = y + 4
    family = z.terms
    assert x in family
    assert Var() not in family


@pytest.mark.skip
@pytest.mark.parametrize("op", [oper.le, oper.lt, oper.ge, oper.gt, oper.eq],
                         ids=['le', 'lt', 'ge', 'gt', 'eq'])
def test_constraint_ancestors(op):
    x, y = Var(), Var()
    constr = op(x + y, 1)
    variables = constr.get_ancestors()
    assert any([v is y for v in variables])
    assert any([v is x for v in variables])
