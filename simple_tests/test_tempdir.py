# content of test_tmpdir.py
import os
import os


def test_create_file(tmpdir):
    print("root: ", tmpdir.get_temproot())
    print("dir(tmpdir)")
    print(dir(tmpdir))
    print()
    print("tmpdir.dirname: ", tmpdir.dirname)
    print("tmpdir.dirpath: ", tmpdir.dirpath())
    print("tmpdir.dump: ", os.listdir(tmpdir))
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1
    assert 0
