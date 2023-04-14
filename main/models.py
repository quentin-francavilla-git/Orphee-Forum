from django.db import models
from django.utils import timezone
class TopicList(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.TextField(default=None)
    title = models.TextField(default=None)
    message = models.TextField(default=None)
    date = models.DateTimeField(auto_now_add=True)
    anonymous = models.BooleanField(default=True)
class TopicsMsg(models.Model):
    id = models.AutoField(primary_key=True)
    idTopic = models.IntegerField(default=None)
    author = models.TextField(default=None)
    message = models.TextField(default=None)
    date = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

class PrivateMessages(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.TextField(default=None)
    receiver = models.TextField(default=None)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default=None)

class Tokens(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.TextField(default=None)
    user_mail = models.TextField(default=None)
    valid_until = models.DateTimeField(auto_now_add=False)
