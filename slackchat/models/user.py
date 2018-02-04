from django.db import models
from slackchat.conf import settings


class User(models.Model):
    """
    A Slack user who posts in a slackchat channel.
    """

    api_id = models.CharField(max_length=50)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to=settings.USER_IMAGE_UPLOAD_TO)
    title = models.CharField(max_length=255)

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
