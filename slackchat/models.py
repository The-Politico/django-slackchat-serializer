from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from markdown import markdown
from slackclient import SlackClient

TOKEN = getattr(settings, 'SLACKCHAT_SLACK_API_TOKEN', None)


class User(models.Model):
    api_id = models.CharField(max_length=50)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)


class Channel(models.Model):
    def fetch_slack_users():
        client = SlackClient(TOKEN)
        response = client.api_call("users.list")
        return [
            (m.get('id'), m.get('profile').get('email'))
            for m in response.get("members")
            if not m.get('deleted') and
            m.get('profile', {}).get('email', False)
        ]

    api_id = models.SlugField(
        max_length=10, null=True, blank=True, editable=False)

    name = models.CharField(
        max_length=150, blank=True, null=True, editable=False)
    owner = models.CharField(max_length=200, choices=fetch_slack_users())

    def __str__(self):
        return 'slackchat-{}'.format(self.name)


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
