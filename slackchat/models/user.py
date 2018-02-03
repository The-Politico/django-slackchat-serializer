from django.db import models
from slackchat.models import RoleAssignment


class User(models.Model):
    """
    A Slack user who posts in a slackchat channel.
    """

    api_id = models.CharField(max_length=50)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField()
    title = models.CharField(max_length=255)

    def get_channel_assignments(self, channel):
        assignments = RoleAssignment.objects.filter(
            user=self,
            channel=channel
        )

        return assignments

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
