class Var(object):

    def __init__(self, name=None):
        self.name = name or id(self)
        self.value = None
