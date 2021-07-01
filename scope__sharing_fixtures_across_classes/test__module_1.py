# content of test_module.py
from smtplib import SMTPException


def test_1(smtp_connection, horses):
    response, msg = smtp_connection.ehlo()
    print(response)
    print(msg)
    assert response == 250
    assert b"smtp.gmail.com" in msg

    assert 0  # for demo purposes


def test_2(smtp_connection):
    response, msg = smtp_connection.noop()
    print(response)
    print(msg)

    assert response == 250
    assert 0  # for demo purposes
