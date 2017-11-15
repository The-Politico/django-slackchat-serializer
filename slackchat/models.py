from django.db import models
from django.utils.safestring import mark_safe

from markdown import markdown


class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)


class Channel(models.Model):
    id = models.CharField(max_length=50, primary_key=True)

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)


class Message(models.Model):
    timestamp = models.DateTimeField(unique=True)

    channel = models.ForeignKey(Channel, related_name='messages')
    user = models.ForeignKey(User, related_name='messages')
    text = models.TextField()

    def html(self):
        return mark_safe(markdown(self.text))

    def __str__(self):
        return str(self.html())


class Reaction(models.Model):
    timestamp = models.DateTimeField(unique=True)

    message = models.ForeignKey(Message, related_name='reactions')
    reaction = models.CharField(max_length=150)
