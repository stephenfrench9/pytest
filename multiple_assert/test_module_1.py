import pytest

class TestMultipleAsserts:
    """
    This fixture comprises the 'Arrange' step (Arrange, Act, Assert, Cleanup)
    """
    @pytest.fixture(scope='class')
    def test_data(self):
        return []

    """
    This fixture comprises the 'Act' step (Arrange, Act, Assert, Cleanup)
    You could argue that this is an "Arrange" step, but lets say that
    we are testing the extend method of python lists.     
    """
    @pytest.fixture(scope='class', autouse='True')
    def act(self, test_data):
        print('running act logic')

        test_data.extend([0, 1, 2, 3, 4])
        return test_data

    """
    These tests are the Assert step (Arrange, Act, Assert, Cleanup)
    """
    def test_0(self, test_data):
        assert test_data[0] == 99

    def test_1(self, test_data):
        assert test_data[1] == 1

    def test_2(self, test_data):
        assert test_data[2] == 2

    def test_3(self, test_data):
        assert test_data[3] == 99

    def test_4(self, test_data):
        assert test_data[4] == 4