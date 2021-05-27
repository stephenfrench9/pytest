import pytest
import datetime

"""
Because of the decorator, this function now runs as a part of "setup". 
As a result, there is a fixture with the same name, 
and the value is the same as the return value, ultimately available for reference in any of the tests in this file.
"""
@pytest.fixture(scope='module')
def module_file(tmpdir_factory):
    now = datetime.datetime.now().microsecond
    print(f"module_file fixture is instantiated: {now}")
    important_sentence = "dont buy Tesla stock"
    fn = tmpdir_factory.mktemp('data').join('img.txt')
    fn.write(important_sentence)

    filename = tmpdir_factory.mktemp("folder").join("example.txt")
    filename.write(f"{now}\nwritten during setup into folder0/example.txt")
    filename = tmpdir_factory.mktemp("folder").join("example.txt")
    filename.write(f"{now}\nwritten during setup into folder1/example.txt")

    return fn
