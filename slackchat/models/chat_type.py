from django.db import models
from foreignform.models import ForeignFormBaseModel


class ChatType(ForeignFormBaseModel):
    """
    A type of slackchat.
    """

    name = models.SlugField(max_length=255)
    publish_path = models.CharField(
        default='/slackchats/',
        max_length=300,
        help_text="A relative path for the slackchat type \
        you can append to any slackchat channel's \
        publish path, e.g., \
        <span style='color:grey; font-weight:bold;'>/slackchats/\
        </span>."
    )
    render_to_html = models.BooleanField(
        default=False,
        help_text="Whether to render markdown to HTML in the serializer.")
    kwargs_in_threads = models.BooleanField(
        default=True,
        help_text="Whether users can create kwargs in threads."
    )

    def __str__(self):
        return self.name
