# https://docs.pytest.org/en/6.2.x/fixture.html#autouse-fixtures-fixtures-you-don-t-have-to-request

import pytest


@pytest.fixture
def string0():
    return "a"


@pytest.fixture(scope='module')
def list0():
    return []


@pytest.fixture(autouse=True)
def append0(list0, string0):
    return list0.append(string0)


def test_1(list0, string0):
    assert list0 == [string0]


def test_2(list0, string0):
    assert list0 == [string0]

