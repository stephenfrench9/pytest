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
