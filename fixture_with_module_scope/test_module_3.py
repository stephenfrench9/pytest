import os

def test_1__module_3(tmpdir_factory):
    directory = tmpdir_factory.getbasetemp()

    fo = open(os.path.join(directory, 'stocks0/advice.txt'))
    print("test_1__module_3: ", fo.read())

    assert 0
