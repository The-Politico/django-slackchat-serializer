import os
import uuid
from datetime import datetime
from urllib.parse import urljoin

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import escape_uri_path
from django.utils.safestring import mark_safe
from markdown import markdown
from slackchat.conf import settings
from slackchat.fields import MarkdownField


class Channel(models.Model):
    """
    A Slack channel that hosts a slackchat.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    api_id = models.SlugField(
        max_length=10,
        null=True,
        blank=True,
        editable=False,
        help_text="Slack API channel ID",
    )

    team_id = models.SlugField(
        max_length=10,
        null=True,
        blank=True,
        editable=False,
        help_text="Slack API team ID",
    )

    chat_type = models.ForeignKey("ChatType", on_delete=models.PROTECT)

    owner = models.ForeignKey("slackchat.User", on_delete=models.PROTECT)

    title = models.CharField(max_length=150, blank=True, null=True)

    introduction = MarkdownField(
        blank=True,
        null=True,
        help_text="Some introductory paragraph text (in markdown syntax).",
    )

    meta_title = models.CharField(
        max_length=300, blank=True, null=True, help_text="Page title"
    )
    meta_description = models.CharField(
        max_length=300, blank=True, null=True, help_text="Page description"
    )
    meta_image = models.URLField(
        blank=True, null=True, help_text="Share image URL"
    )

    # Extra metadata, provided by django-foreignform
    extras = JSONField(blank=True, null=True)

    publish_path = models.CharField(
        max_length=300,
        blank=True,
        unique=True,
        help_text="A relative path you can use when \
        publishing the slackchat, e.g., \
        <span style='color:grey; font-weight:bold;'>/2018-02-12/econ-chat/\
        </span>.",
    )

    publish_time = models.DateTimeField(
        null=True, blank=True, help_text="Dateline."
    )

    published = models.BooleanField(
        default=False,
        help_text="Determines if the page should be live (for renderer)",
    )

    live = models.BooleanField(
        default=False,
        help_text="Determines whether page should re-poll for new messages \
        while chat is live.",
    )

    @property
    def published_link(self):
        if settings.PUBLISH_ROOT:
            relative_path = os.path.join(
                self.chat_type.publish_path, self.publish_path.lstrip("/")
            ).lstrip("/")
            link = urljoin(settings.PUBLISH_ROOT, relative_path)
            return mark_safe(
                '<a href="{0}" target="_blank">{0}</a>'.format(link)
            )
        else:
            return os.path.join(
                self.chat_type.publish_path, self.publish_path.lstrip("/")
            )

    @property
    def api_link(self):
        link = reverse("slackchat-channel-detail", args=[self.id])
        return mark_safe('<a href="{0}" target="_blank">{0}</a>'.format(link))

    @property
    def slack_link(self):
        if self.team_id:
            return mark_safe(
                '<a href="slack://channel?id={0}&team={1}"\
                 target="_blank">{2}</a>'.format(
                    self.api_id, self.team_id, self.slackchat
                )
            )
        else:
            return "-"

    @property
    def slackchat(self):
        return "slackchat-{}".format(self.id.hex[:10])

    def save(self, *args, **kwargs):
        if self.publish_path:
            self.publish_path = escape_uri_path(self.publish_path)
        else:
            self.publish_path = "/{}/{}/".format(
                datetime.today().strftime("%Y-%m-%d"), self.id.hex[:8]
            )
        super().save(*args, **kwargs)

    def get_introduction(self):
        if self.chat_type.render_to_html:
            return mark_safe(markdown(self.introduction))
        return self.introduction

    def __str__(self):
        return self.slackchat
