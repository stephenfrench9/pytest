import pytest
import os

def test_0(list0):
    filename = os.path.basename(__file__)
    list0.append(filename)
    assert list0 == [os.path.basename(__file__)]
    assert 0
