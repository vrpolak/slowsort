# Nothing important here, just me being sad about PEP 3140.

class StrT1(object):

    def __init__(self, one, two):
        self.one = one
        self.two = two

    def __str__(self):
        return "StrT1(" + str(self.one) + ")"

class StrT2(object):

    def __init__(self, one, two):
        self.one = one
        self.two = two

    def __str__(self):
        return "StrT2(" + str(self.one) + ")"

    def __repr__(self):
        return "StrT2(" + repr(self.one) + ", " + repr(self.two) + ")"


wrap = StrT1(1, 2)
assert "StrT1(1)" == str(wrap)

wrap = StrT2(1, 2)
assert "StrT2(1)" == str(wrap)

wrap = StrT2(StrT2(1, 0), StrT1(2, 0))
assert "StrT2(StrT2(1))" == str(wrap)

wrap = [StrT1(1, 3), StrT2(2, 4)]
assert "[StrT1(1),StrT2(2)]" == str(wrap), str(wrap)
