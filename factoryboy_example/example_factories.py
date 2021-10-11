from django.contrib.auth.models import User
from factory import post_generation
import factory
import os


# Basic Usage


class ExampleUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "default"
    password = "default"
    is_superuser = True
    is_staff = True
    email = "default"


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

    email = "john"

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
        obj.username = "default_" + str(obj.id)


# lazy functions
def password():
    return "default--from-lazy-function"


class ExampleUserFactory_lazyfunction(ExampleUserFactory):
    password = factory.LazyFunction(password)


# lazy attributes
class lazyattribute(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "lazy_user"
    password = "lazy_pw"
    is_superuser = True
    is_staff = True
    email = "lazy_email"

    @factory.lazy_attribute
    def email(self):
        return f"{self.username}@gmail.com"


class lazyattribute_reflexive(lazyattribute):
    @factory.lazy_attribute
    def email(self):
        return f"{self.email}@gmail.com"


class lazyattribute_id(lazyattribute):
    @factory.lazy_attribute
    def email(self):
        return f"{self.username}-{self.id}@gmail.com"


## Comon recipes
from polls.models import Group


# from mysite.polls.models import Group


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"Group{n}")


from polls.models import Suser
# from mysite.polls.models import Suser
class SuserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Suser

    name = factory.Sequence(lambda n: "Agent %03d" % n)
    group = factory.SubFactory(GroupFactory)


class DraftedSuserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Suser

    name = factory.Sequence(lambda n: "Suser{n}")
    group = factory.Iterator(Group.objects.all())


class AutomaticallyPopulatedGroup_Factory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    @factory.sequence
    def name(self, n):
        return f'group{n}'

    # read this field not as a field on the the Product, but as a whole new object.
    user_dummy_name = factory.RelatedFactory(SuserFactory, factory_related_name='group')
    # factory_related_name identifies a Foreign Key Field
    # The id for Products of this factory (self, not the RelatedFactory) is gonna be stored in what field of what object?
    # Well you dentify the object with the first argument, and the field with the second.

from polls.models import PromiscuousUser
from polls.models import Group
class PromiscuousUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PromiscuousUser

    @factory.sequence
    def name(n):
        return f"PromiscuousUser{n}"

    @factory.post_generation
    def anything(self, create, extracted, **kwargs):  # the name of the callback doesn't matter
        if not create:
            return
        g1 = Group(name='g1')
        g2 = Group(name='g2')
        g1.save()
        g2.save()
        print(self.name)
        self.group.add(g1)
        self.group.add(g2)

# class PromiscuousUser(models.Model):
#     name = models.CharField(max_length=300)
#     group = models.ManyToManyField(Group, on_delete=models.CASCADE, null=True)

## Common recipes
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
        inline_args = ("first_position", "second_position", "third_position")

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
        old = factory.Trait(
            begin=datetime.date(1900, 1, 1), end=datetime.date(1900, 1, 3)
        )
