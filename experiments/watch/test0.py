import time

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command

from polls.models import Question
from polls.models import Question



@pytest.fixture()
@pytest.mark.django_db(transaction=True)
def django_db_setup(django_db_setup, django_db_blocker, transactional_db):
    test_db = '/Users/stephen.french/pytest-examples/mysite/db.sqlite3'
    from django.conf import settings
    settings.DATABASES['default']['NAME'] = test_db
    settings.DATABASES['default']['CONN_MAX_AGE'] = 60
    # run_sql(f'DROP DATABASE IF EXISTS {test_db}')
    # run_sql(f'CREATE DATABASE {test_db}')
    with django_db_blocker.unblock():
            User.objects.create_user('jdango_db_setup', password='bar')
            Question(question_text='djangopdb-setup,django-db-blocker').save()


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def insert_into(settings, transactional_db):
    print(settings.DATABASES)
    Question(question_text='insert-fixtuer').save()


@pytest.mark.django_db
def test0(settings, insert_into):
    time.sleep(100)
    assert 0
    return
