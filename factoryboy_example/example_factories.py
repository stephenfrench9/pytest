from django.contrib.auth.models import User
from factory import post_generation
import factory
import os



# Basic Usage

class ExampleUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'default'
    password = 'default'
    is_superuser = True
    is_staff = True
    email = 'default'


# Sequences

class ExampleUserFactory_sequence(ExampleUserFactory):

    @factory.sequence
    def username(n):
        new = f'{"default_"}{str(n)}'
        print("orca")
        print(new)
        return new


class ExampleUserFactory_one_sequence(ExampleUserFactory_sequence):

    @factory.sequence
    def id(n):
        return n


# Post Generation Hooks
class UserFactory_PostGeneration(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = 'john'

    @post_generation
    def any_word_will_do(obj, create, extracted, **kwargs):
        print("The Post Generation hook is running.")
        print("The objects and values available to this callback (hook) are:")
        print("type(obj): ", type(obj))
        print("create: ", create)
        print("extracted: ", extracted)
        print("kwargs: ", kwargs)
        print("The Post Generation hook is completed")
        return "Irrelevant return statement"


class Unique(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    @post_generation
    def set_username(obj, create, extracted, **kwargs):
        print("extrac: ", extracted)
        print("id: ", obj.id)
        obj.username = 'default_' + str(obj.id)


# lazy functions
def password():
    return 'default--from-lazy-function'


class ExampleUserFactory_lazyfunction(ExampleUserFactory):
    password = factory.LazyFunction(password)

# lazy attributes
class ExampleUserFactory_lazyattribute(ExampleUserFactory_lazyfunction):
    @factory.lazy_attribute
    def email(self):
        return f'{self.username}@gmail.com'

class ExampleUserFactory_lazyattribute2(ExampleUserFactory_lazyfunction):
    @factory.lazy_attribute
    def email(self):
        return f'{self.username}-{self.id}@gmail.com'



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
    end = factory.LazyAttribute(lambda o: o.begin + datetime.timedelta(days=o.duration))

    class Params:
        duration = 5
        old = factory.Trait(begin=datetime.date(1900, 1, 1), end=datetime.date(1900, 1, 3))
