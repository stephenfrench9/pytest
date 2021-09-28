import pytest


def f():
    raise SystemExit(1)


def test_my_test():
    with pytest.raises(SystemExit):
        f()
