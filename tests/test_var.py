from pybip.variables import Var


def test_var_initializes_with_name():
    x = Var('x')
    assert x.name == 'x'
