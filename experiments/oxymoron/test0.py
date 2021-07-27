import pytest
from django.contrib.auth.models import User


@pytest.fixture(scope='class')
def fixture0():
    alto = User.objects.create_user('foo', password='foo')
    return

@pytest.mark.django_db
def test0(fixture0):
    return
