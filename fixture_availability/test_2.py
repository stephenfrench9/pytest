"""
This test module has three classes, each with one test.

A given test requests the 'list0' fixture, and so has a list
available to that test and isolated from other tests. Restated,
there is a fixture object scoped to the test.

A given test also requests a fixture called 'addend'.
The test finds the fixture in the module scope. The addend fixture
requests the string0 fixture. There are three string0 fixture functions
to choose from to use to instantiate the fixture. The fixture function
in the same scope at the original requesting function (the class scope)
is chosen over the fixture function in the parent (umbrella) scope which
happens to be the native scope for the requesting function. This is
the situation of a fixture requesting a fixture, which follows a different
set of rules to locate said fixture than does the case of a function requesting
a fixture. But we see here a preference for the fixture definition in the smaller,
child scope.
"""

import pytest


@pytest.fixture(scope="function")
def list0():
    return []


@pytest.fixture
def addend(string0):
    pass


@pytest.fixture
def string0(list0):
    list0.append("string0")


class TestOne:
    @pytest.fixture
    def string0(self, list0):
        list0.append("TestOne Overwrite")


    def test_1(self, list0, addend):
        assert list0 == ["TestOne Overwrite"]


class TestTwo:
    def test_1(self, list0, addend):
        assert list0 == ["string0"]


class TestThree:
    def test_1(self, list0, addend):
        assert list0 == ["string0"]
