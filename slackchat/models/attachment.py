from django.db import models


class Attachment(models.Model):
    """
    An attachment to a Slack message.
    """
    message = models.ForeignKey(
        'Message', related_name='attachments', on_delete=models.CASCADE)

    title = models.CharField(max_length=300, blank=True, null=True)
    title_link = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    service_name = models.CharField(max_length=300, blank=True, null=True)
    service_icon = models.URLField(blank=True, null=True)
    service_url = models.URLField(blank=True, null=True)

    image_url = models.URLField(blank=True, null=True)
    image_width = models.PositiveSmallIntegerField(blank=True, null=True)
    image_height = models.PositiveSmallIntegerField(blank=True, null=True)

    video_html = models.TextField(blank=True, null=True)
    video_html_width = models.PositiveSmallIntegerField(blank=True, null=True)
    video_html_height = models.PositiveSmallIntegerField(blank=True, null=True)

    thumb_url = models.URLField(blank=True, null=True)
    thumb_width = models.PositiveSmallIntegerField(blank=True, null=True)
    thumb_height = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title_link or self.image_url

    class Meta:
        unique_together = (
            ('message', 'title_link', 'image_url'),
        )
