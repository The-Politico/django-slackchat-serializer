from django.db import models
from slackchat.conf import settings
from slackclient import SlackClient


class Channel(models.Model):
    """
    A Slack channel that hosts a slackchat.
    """

    def fetch_slack_users():
        client = SlackClient(settings.SLACK_API_TOKEN)
        response = client.api_call("users.list")
        return [
            (m.get('id'), m.get('profile').get('email'))
            for m in response.get("members")
            if not m.get('deleted') and
            m.get('profile', {}).get('email', False)
        ]

    api_id = models.SlugField(
        max_length=10, null=True, blank=True, editable=False)
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    keywords = models.CharField(max_length=300, blank=True, null=True)
    name = models.CharField(
        max_length=150, blank=True, null=True, editable=False)
    owner = models.CharField(max_length=200, choices=fetch_slack_users())
    chat_type = models.ForeignKey(
        'ChatType', on_delete=models.PROTECT)

    def __str__(self):
        return 'slackchat-{}'.format(self.name)
