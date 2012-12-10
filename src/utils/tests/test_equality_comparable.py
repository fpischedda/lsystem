from utils.equality_comparable import EqualityComparable


class A(EqualityComparable):

    def __init__(self, value):

        self.value = value


class B(A):
    pass


class C(object):

    def __init__(self, value):

        self.value = value


def test_comparable_same_class():

    a1 = A(1)
    a2 = A(1)

    assert a1 != a2


def test_comparable_derived_class():

    a = A(1)
    b = B(1)

    assert a != b


def test_comparable_vs_not_derived_class():

    a = A(1)
    c = C(1)

    assert a != c
