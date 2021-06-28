def test_0(settings):
    print("---------------------------"
          "Output from test module: \'test_plugin\'::test_0."
          "---------------------------", end="\n\n")
    print("settings.ROOT_URLCONF: ", settings.ROOT_URLCONF)
    print()
    print("settings.WSGI_APPLICATION: ", settings.WSGI_APPLICATION)
    print()
    print("settings.DEBUG: ", settings.DEBUG)
    print("-------------------------------------------------------------------------------------------------------")
    assert 0

def test_1(settings):
    settings.DEBUG = True
    assert 0

def test_2(settings):
    assert settings.DEBUG == True