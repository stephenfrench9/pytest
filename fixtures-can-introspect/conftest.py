import pytest
import smtplib


@pytest.fixture(scope="function")
def smtp_connection(request):
    func = request.function
    mod = request.module
    vars_and_funcs = [a for a in dir(mod) if a[0] != '_' and a[0] != '@']
    print(f"This fixture was requested by function: {func.__name__}")
    print(f"This fixture was requested from the module: {mod.__name__}")
    print(f"The module from which this fixture was requested offers these variables and functions: {vars_and_funcs}")

    server = getattr(request.module, "smtpserver", "smtp.gmail.com")
    smtp_connection = smtplib.SMTP(server, 587, timeout=5)
    yield smtp_connection
    print("finalizing {} ({})".format(smtp_connection, server))
    smtp_connection.close()


@pytest.fixture(scope="module")
def smtp_connection__module_scope(request):
    func = request.function
    print(f"This fixture was requested by function: {func.__name__}")

    server = getattr(request.module, "smtpserver", "smtp.gmail.com")
    smtp_connection = smtplib.SMTP(server, 587, timeout=5)
    yield smtp_connection
    print("finalizing {} ({})".format(smtp_connection, server))
    smtp_connection.close()
