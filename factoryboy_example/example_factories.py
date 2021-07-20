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
