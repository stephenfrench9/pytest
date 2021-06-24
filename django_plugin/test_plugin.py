def test_0(settings):
    print("---------------------------"
          "Output from test module: \'test_plugin\'::test_0."
          "---------------------------", end="\n\n")
    print("settings.MIDDLEWARE: ", settings.MIDDLEWARE)
    print()
    print("settings.CUSTOM_SETTING: ", settings.CUSTOM_SETTING)
    print("-------------------------------------------------------------------------------------------------------")
    assert 0