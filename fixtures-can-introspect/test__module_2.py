smtpserver = "smtp.mail.yahoo.com"  # will be read by smtp fixture


def test_1(smtp_connection):
    a = 1
    assert 0, smtp_connection.helo()


def test_2(smtp_connection__module_scope):
    assert 0, smtp_connection__module_scope.helo()
