# content of test_anothersmtp.py

smtpserver = "mail.python.org"  # will be read by smtp fixture

variable1 = "module 1 a"
variable2 = "module 1 b"


def test_1(smtp_connection):
    assert 0, smtp_connection.helo()

def test_2(smtp_connection__module_scope):
    assert 0, smtp_connection__module_scope.helo()
