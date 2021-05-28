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
    print(f"The 'module_file' fixture is instantiated at {now}")
    advice = "dont buy Tesla stock"
    fn = tmpdir_factory.mktemp('stocks').join('advice.txt')
    fn.write(advice)

    return fn
