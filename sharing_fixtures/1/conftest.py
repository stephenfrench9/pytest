import pytest

@pytest.fixture(scope = 'module')
def list0():
    return []