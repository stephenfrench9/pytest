import pytest


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_recursion_depth():
    with pytest.raises(RuntimeError) as excinfo:
        def f():
            f()

        f()
    print(str(excinfo.value))
    assert 'recursion' in str(excinfo.value)


def afunc():
    raise AssertionError('anythin')


def test_for_certain_error():
    """
    There is more to the exception than the name.
    :return:
    """
    with pytest.raises(AssertionError) as excinfo:
        afunc()
    assert 'anythin' in str(excinfo.value)


def test_for_certain_error_way_2():
    """
    There is more to the exception than the name.
    :return:
    """
    with pytest.raises(AssertionError, match='anythin'):
        afunc()
