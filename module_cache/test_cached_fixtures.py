"""
https://docs.pytest.org/en/6.2.x/fixture.html#fixtures-can-be-requested-more-than-once-per-test-return-values-are-cached

Fixtures are cached.
If they are scoped to the module, then they are called ONLY ONCE per module.

Note the fixture called 'append' is requested by two tests in this module.
Despite being twice requested, it is only once instantiated.
Restated, the fixture provided to both tests
is the same object (id(append_second) evaluates to the same value)

"""

import pytest


@pytest.fixture(scope='module')
def string0():
    print("fixture called: first_entry")
    return "a"


@pytest.fixture(scope='module')
def list0():
    print("fixture called: order")
    return []


@pytest.fixture(scope='module')
def append(list0, string0):
    print("fixture called: append")
    list0.append(string0)
    return list0


def test_initiate_side_effects(append):
    print("Running first test")
    print("id(append): ", id(append))
    assert 0


def test_side_effect(append, string0):
    print("Running second test")
    print("id(append): ", id(append))
    assert append == [string0]
    assert 0
