import pytest
from django.contrib.auth.models import User


@pytest.fixture
def fixture_A():
    user = User.objects.create_user('fixture_A', password='fixture_A')
    return


@pytest.fixture()
def fixture_B():
    user = User.objects.create_user('fixture_B', password='fixture_B')
    return

@pytest.mark.django_db
def test_A(fixture_A):
    userA = User.objects.get(username='fixture_A')
    assert userA.username == 'fixture_A'

    with pytest.raises(Exception):
        userB = User.objects.get(username='fixture_B')

    return

@pytest.mark.django_db
def test_B(fixture_B):
    with pytest.raises(Exception):
        userA = User.objects.get(username='fixture_A')

    userB = User.objects.get(username='fixture_B')
    assert userB.username == 'fixture_B'

    return
