from django.db import models
from django.contrib.postgres.fields import JSONField


class CustomContentTemplate(models.Model):
    """
    Defines search parameters for finding custom messages
    and a template for how to serialize the message.
    """

    name = models.CharField(max_length=255)
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
    argument_template = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        help_text="A comma seprated list of Python format string whose \
        args are the capture groups matched by the search_string.",
    )
    attachment_template = JSONField(
        blank=True,
        null=True,
        help_text="A JSON object added to a message's attachments whose \
        values may be Python formatted strings. The args given to formatted \
        strings are the capture groups matched by the search string.",
    )
    kwarg_template = JSONField(
        blank=True,
        null=True,
        help_text="A JSON object added to a message's kwargs whose values may \
        be Python formatted strings. The args given to formatted strings are \
        the capture groups matched by the search string.",
    )

    def __str__(self):
        return self.name
