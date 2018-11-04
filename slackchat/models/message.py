import re

from django.contrib.postgres.fields import JSONField
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
        "Channel", related_name="messages", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "User", related_name="messages", on_delete=models.CASCADE
    )
    text = models.TextField()

    serialized = JSONField(blank=True, null=True)

    def html(self):
        return mark_safe(markdown(self.get_content()))

    def get_content(self):
        template, match = self.find_template_match()
        if template and template.content_template != "" and match:
            groups = [group for group in match.groups()]
            return template.content_template.format(*groups)
        return self.text

    def get_custom_args(self):
        template, match = self.find_template_match()
        if match:
            groups = [group for group in match.groups()]
            return [
                str(arg).strip().format(*groups)
                for arg in template.argument_template.split(",")
            ]
        return None

    def get_custom_kwargs(self):
        return self.parse_json_template("kwarg_template")

    def get_custom_attachment(self):
        return self.parse_json_template("attachment_template")

    def parse_json_template(self, template_type):
        template_schema, match = self.find_template_match()
        if match:
            groups = [group for group in match.groups()]
            output_dict = dict()
            template = getattr(template_schema, template_type)
            if isinstance(template, dict):
                for key in template:
                    template_key = getattr(template_schema, template_type)[key]
                    if isinstance(template_key, str):
                        output_dict[key] = template_key.format(*groups)
                    else:
                        output_dict[key] = template_key
                return output_dict
        return None

    def find_template_match(self):
        for template in CustomContentTemplate.objects.filter(
            chat_type=self.channel.chat_type
        ):
            match = re.search(template.search_string, self.text)
            if match:
                return (template, match)
        return (None, None)

    def serialize(self):
        self.save()

    def save(self, *args, **kwargs):
        from slackchat.serializers import MessageSerializer

        self.serialized = MessageSerializer(self).data
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:50]
