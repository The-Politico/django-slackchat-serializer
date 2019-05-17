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
        running_text = self.text
        matches = self.find_template_matches()

        if len(matches) > 0:
            for template, _ in matches:
                if template and template.content_template != "":
                    groups = [
                        group
                        for group in re.search(
                            template.search_string, running_text
                        ).groups()
                    ]
                    running_text = template.content_template.format(*groups)
        return running_text

    def get_custom_args(self):
        custom_args = []
        matches = self.find_template_matches()

        for template, match in matches:
            if match and template.argument_template:
                custom_args = [
                    str(arg).strip().format(*match.groups())
                    for arg in template.argument_template.split(",")
                ] + custom_args

        return custom_args

    def get_custom_kwargs(self):
        return self.parse_json_template("kwarg_template")

    def get_custom_attachment(self):
        return self.parse_json_template("attachment_template")

    def parse_json_template(self, template_type):
        output_dict = dict()

        matches = self.find_template_matches()
        if len(matches) > 0:
            for template_schema, match in matches:
                if match:
                    groups = [group for group in match.groups()]
                    template = getattr(template_schema, template_type)
                    if isinstance(template, dict):
                        for key in template:
                            template_key = getattr(
                                template_schema, template_type
                            )[key]
                            if isinstance(template_key, str):
                                output_dict[key] = template_key.format(*groups)
                            else:
                                output_dict[key] = template_key

        return output_dict

    def find_template_matches(self):
        matches = []

        for template in CustomContentTemplate.objects.filter(
            chat_type=self.channel.chat_type
        ):
            match = re.search(template.search_string, self.text)
            if match:
                matches.append((template, match))
        return matches

    def serialize(self):
        self.save()

    def save(self, *args, **kwargs):
        from slackchat.serializers import MessageSerializer

        self.serialized = MessageSerializer(self).data
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:50]
