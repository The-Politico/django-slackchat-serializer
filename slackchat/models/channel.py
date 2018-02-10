import re
import uuid
from datetime import datetime
from urllib.parse import urljoin

from django.db import models
from django.utils import timezone
from django.utils.encoding import escape_uri_path
from django.utils.safestring import mark_safe
from markdown import markdown
from slackchat.conf import settings
from slackchat.fields import MarkdownField
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    api_id = models.SlugField(
        max_length=10, null=True, blank=True, editable=False)

    chat_type = models.ForeignKey(
        'ChatType', on_delete=models.PROTECT)

    owner = models.CharField(max_length=200, choices=fetch_slack_users())

    title = models.CharField(max_length=150, blank=True, null=True)

    image = models.ImageField(
        upload_to=settings.CHANNEL_IMAGE_UPLOAD_TO, blank=True, null=True,
        help_text="An image to feature on the rendered Slackchat page.")

    introduction = MarkdownField(
        blank=True, null=True,
        help_text="Some introductory paragraph text in markdown syntax.")

    meta_title = models.CharField(
        max_length=300, blank=True, null=True,
        help_text="Title for page meta data.")
    meta_description = models.CharField(
        max_length=300, blank=True, null=True,
        help_text="Description for page meta data.")
    meta_keywords = models.CharField(
        max_length=300, blank=True, null=True,
        help_text="Keywords for page meta data.")

    publish_path = models.CharField(
        max_length=300, blank=True, unique=True,
        help_text="A relative path that a renderer may use when \
        publishing the slackchat, e.g., \
        <span style='color:grey; font-weight:bold;'>/2018-02-12/econ-chat/\
        </span>."
    )

    publish_time = models.DateTimeField(
        default=timezone.now, help_text="May be used by renderer to \
        create dateline.")

    live = models.BooleanField(
        default=False, help_text="May be used by renderer to determine\
        if it should repoll for messages while chat is live.")

    @property
    def published_link(self):
        if settings.PUBLISH_ROOT:
            relative_path = re.sub('^/', '', self.publish_path)
            link = urljoin(settings.PUBLISH_ROOT, relative_path)
            return mark_safe(
                '<a href="{0}" target="_blank">{0}</a>'.format(link))
        else:
            return self.publish_path

    @property
    def slack_channel(self):
        return 'slackchat-{}'.format(self.id.hex[:10])

    def save(self, *args, **kwargs):
        if self.publish_path:
            self.publish_path = escape_uri_path(self.publish_path)
        else:
            self.publish_path = '/{}/{}/'.format(
                datetime.today().strftime('%Y-%m-%d'),
                self.id.hex[:8]
            )
        super().save(*args, **kwargs)

    def get_introduction(self):
        if self.chat_type.render_to_html:
            return mark_safe(markdown(self.introduction))
        return self.introduction

    def __str__(self):
        return self.slack_channel
