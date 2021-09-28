# content of test_assert2.py


def test_set_comparison():
    set1 = set("308")
    set2 = set("803")
    assert set1 == set2

    dict1 = {'a': 1, 'b': 2, 't': {}}
    dict2 = {'a': 1, 'c': 4, 'b': 3}
    assert dict1 == dict2
