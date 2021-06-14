import pytest

def test_0(list0):
    print(list0)
    assert list0 == ["0"]

class TestHiddenFixture:

    def test_1(self, list0):
        print(list0)
        assert list0 == ["0"]

    @pytest.fixture(scope='session')
    def list0(self):
        return ["0"]
