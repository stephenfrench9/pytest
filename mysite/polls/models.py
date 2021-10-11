from django.db import models

# Create your models here.
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)

# from polls.models import Group
class Group(models.Model):
    name = models.CharField(max_length=200)

# from polls.models import Suser
class Suser(models.Model):
    name = models.CharField(max_length=300)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

# from polls.models import PromiscuousUser
class PromiscuousUser(models.Model):
    name = models.CharField(max_length=300)
    group = models.ManyToManyField(Group, null=True)
