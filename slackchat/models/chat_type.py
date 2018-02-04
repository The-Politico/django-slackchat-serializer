from django.db import models


class ChatType(models.Model):
    """
    A type of slackchat.
    """

    name = models.CharField(max_length=255)
    render_to_html = models.BooleanField(
        default=False,
        help_text="Whether to render markdown to HTML in the serializer.")

    def __str__(self):
        return self.name
