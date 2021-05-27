import os

def test_1__module_3(tmpdir_factory):
    directory = tmpdir_factory.getbasetemp()
    # print(os.listdir(directory))
    fo = open(os.path.join(directory, 'folder0/example.txt'))
    print(fo.read())
    fo = open(os.path.join(directory, 'folder1/example.txt'))
    print(fo.read())
    assert 0
