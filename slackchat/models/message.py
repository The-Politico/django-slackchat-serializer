import re

from django.db import models
from django.utils.safestring import mark_safe
from markdown import markdown

from .custom_content_template import CustomContentTemplate


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
        return mark_safe(markdown(self.get_content()))

    def get_content(self):
        template, match = self.find_template_match()
        if match:
            groups = [group for group in match.groups()]
            return template.content_template.format(*groups)
        return self.text

    def find_template_match(self):
        for template in CustomContentTemplate.objects.filter(
            chat_type=self.channel.chat_type
        ):
            match = re.search(template.search_string, self.text)
            if match:
                return (template, match)
        return (None, None)

    def __str__(self):
        return self.text[:50]
