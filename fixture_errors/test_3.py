import pytest


@pytest.fixture
def list0():
    return []


@pytest.fixture
def first(list0):
    print("first fixture executes")
    raise Exception("The first of three setup fixtures fails")
    list0.append(1)


@pytest.fixture
def second(list0, first):
    print("second fixture executes")
    list0.extend([2])


@pytest.fixture(autouse=True)
def third(list0, second):
    print("third fixture executes")
    list0 += [3]


def test_3(list0):
    assert list0 == [1, 2, 3]

