from django.db import models


class CustomContentTemplate(models.Model):
    """
    Defines search parameters for finding custom messages
    and a template for how to serialize the message.
    """

    name = models.CharField(max_length=255)
    argument_name = models.SlugField(
        max_length=255,
        blank=True, null=True,
        help_text="Add an argument to the message if search_string \
        matches against a message's content.")
    search_string = models.CharField(
        max_length=255,
        help_text="A regex search string with capture groups.")
    chat_type = models.ForeignKey(
        'ChatType', on_delete=models.CASCADE)
    content_template = models.TextField(
        help_text="A Python format string whose args are the capture groups \
        matched by the search_string."
    )

    def __str__(self):
        return self.name
