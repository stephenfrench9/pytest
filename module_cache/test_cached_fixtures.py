
import pytest


@pytest.fixture(scope='module')
def string0():
    print("fixture called: string0")
    return "a"


@pytest.fixture(scope='module')
def list0():
    print("fixture called: list0")
    return []


@pytest.fixture(scope='module')
def append(list0, string0):
    print("fixture called: append")
    list0.append(string0)
    return list0


def test_1(append):
    print("Running first test")
    print("id(append): ", id(append))
    assert 0


def test_2(append, string0):
    print("Running second test")
    print("id(append): ", id(append))
    assert append == [string0]
    assert 0
