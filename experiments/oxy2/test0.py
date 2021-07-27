import pytest
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db

@pytest.fixture(autouse=True)
def fixture0():
    alto = User.objects.create_user('foo', password='foo')
    return


def test0():
    User.objects.get(username='foo')
    return


class TestGroup:
    def test1(self):
        User.objects.get(username='foo')
        return

    def test2(self):
        User.objects.get(username='foo')
        return