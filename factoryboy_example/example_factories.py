from django.contrib.auth.models import User
import factory


class ExampleUserFactory(factory.Factory):
    class Meta:
        model = User

    @factory.sequence
    def id(n):
        return n

    username = 'default'
    password = 'default'
    is_superuser = True
    is_staff = True
    email = 'default'


def password():
    return 'default--from-lazy-function'


class ExampleUserFactory_lazyfunction(ExampleUserFactory):
    password = factory.LazyFunction(password)


class ExampleUserFactory_lazyattribute(ExampleUserFactory_lazyfunction):
    @factory.lazy_attribute
    def email(self):
        return f'{self.username}@gmail.com'


class Mine(object):
    """
    This class can accept three positional arguments.
    """
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class MineFactory(factory.Factory):
    class Meta:
        model = Mine
        inline_args = ('first_position', 'second_position', 'third_position')

    first_position = 1
    second_position = 2
    third_position = 3

class Rental(object):
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

import factory.fuzzy

import datetime

class RentalFactory(factory.Factory):
    class Meta:
        model = Rental

    begin = factory.fuzzy.FuzzyDate(start_date=datetime.date(2000, 1, 1))
    end = factory.LazyAttribute(lambda o: o.begin + o.duration)

    class Params:
        duration = datetime.timedelta(days=5)