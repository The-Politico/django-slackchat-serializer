from django.db import models
from django.utils.safestring import mark_safe
from markdown import markdown


class Message(models.Model):
    """
    A message posted in a Slack channel by a user.
    """

    timestamp = models.DateTimeField(unique=True)

    channel = models.ForeignKey(
        'Channel', related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(
        'User', related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()

    def html(self):
        return mark_safe(markdown(self.text))

    def __str__(self):
        return str(self.html())
