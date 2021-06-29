import pytest

@pytest.mark.django_db
def test_0(settings):
    from django.contrib.auth.models import User
    user = User.objects.create_user('foo', password='bar')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    assert len(User.objects.all()) == 1

    assert 0

@pytest.mark.django_db
def test_1(settings):
    from django.contrib.auth.models import User
    user = User.objects.create_user('foo2', password='bar2')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    assert len(User.objects.all()) == 1

    assert 0
