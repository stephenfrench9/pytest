import pytest
from django.contrib.auth.models import User

@pytest.fixture(scope='module')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.create_user('fixture_A', password='fixture_A')
        User.objects.create_user('fixture_B', password='fixture_B')
    return


@pytest.mark.django_db
def test_A():
    userA = User.objects.get(username='fixture_A')
    assert userA.username == 'fixture_A'
    userB = User.objects.get(username='fixture_B')
    assert userB.username == 'fixture_B'

    return

@pytest.mark.django_db
def test_B():
    userA = User.objects.get(username='fixture_A')
    assert userA.username == 'fixture_A'
    userB = User.objects.get(username='fixture_B')
    assert userB.username == 'fixture_B'

    return
