import pytest

@pytest.fixture(scope = 'package')
def list0():
    return []