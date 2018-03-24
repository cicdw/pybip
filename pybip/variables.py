class Var(object):
    __slots__ = ('name', 'value')

    def __init__(self, name=None):
        self.name = name or id(self)
        self.value = None

    def set_value(self, val):
        self.value = val
