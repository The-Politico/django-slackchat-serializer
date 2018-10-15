from django.db import models
from django.contrib.postgres.fields import JSONField


class CustomContentTemplate(models.Model):
    """
    Defines search parameters for finding custom messages
    and a template for how to serialize the message.
    """

    name = models.CharField(max_length=255)
    argument_name = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Add an argument to the message if search_string \
        matches against a message's content.",
    )
    search_string = models.CharField(
        max_length=255, help_text="A regex search string with capture groups."
    )
    chat_type = models.ForeignKey("ChatType", on_delete=models.CASCADE)
    content_template = models.TextField(
        blank=True,
        null=True,
        help_text="A Python format string whose args are the capture groups \
        matched by the search_string.",
    )
    argument_template = models.TextField(
        blank=True,
        null=True,
        help_text="A Python format string whose args are the capture groups \
        matched by the search_string.",
    )
    attachment_template = JSONField(
        blank=True,
        null=True,
        help_text="A JSON object with Python formatted strings whose args are \
        the capture groups matched by the search_string and added to the \
        message's attachments.",
    )
    kwarg_template = JSONField(
        blank=True,
        null=True,
        help_text="A JSON object with Python formatted strings whose args are \
        the capture groups matched by the search_string and added to the \
        message's kwargs (overridden by manual kwargs in the thread).",
    )

    def __str__(self):
        return self.name
