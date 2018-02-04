from django.db import models


class Webhook(models.Model):
    """
    An endpoint that is hit whenever Slackchat objects
    are created or updated.

    Used to signal reserialization should happen for
    a slackchat renderer.
    """
    endpoint = models.URLField()
    verified = models.BooleanField(default=True)

    def __str__(self):
        return self.endpoint
