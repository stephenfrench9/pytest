# contents of test_append.py
import pytest


# Arrange
@pytest.fixture(scope='module')
def first_entry():
    return "a"


# Arrange
@pytest.fixture(scope='module')
def order(first_entry):
    return [first_entry]


def test_string(list0):
    # Act
    list0.append("b")

    # Assert
    assert list0 == ["a", "b"]


def test_int(list0):
    # Act
    list0.append(2)

    # Assert
    assert list0 == ["a", "b", 2]

# Arrange
@pytest.fixture(scope='function')
def first_entry_iso():
    return "a"


# Arrange
@pytest.fixture(scope='function')
def order_iso(first_entry_iso):
    return [first_entry_iso]


def test_string_iso(order_iso):
    # Act
    order_iso.append("b")

    # Assert
    assert order_iso == ["a", "b"]


def test_int(order_iso):
    # Act
    order_iso.append(2)

    # Assert
    assert order_iso == ["a", 2]
