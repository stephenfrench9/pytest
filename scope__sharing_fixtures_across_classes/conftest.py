# content of conftest.py
import pytest
import smtplib


@pytest.fixture(scope="module")
def smtp_connection():
    print('setting the module scoped fixture called smtp_connection')
    thing = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    return thing

@pytest.fixture
def horses():
    a = {'sammy': 'sarah'}
    return a

