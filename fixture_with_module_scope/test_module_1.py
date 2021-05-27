def test_1__module_1(module_file):
    print("test_1__module_1", module_file.read())
    assert 0


def test_2__module_1(module_file):
    print("test_2__module_1: ", module_file.read())
    assert 0
