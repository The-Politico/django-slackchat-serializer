from django.db import models


class Webhook(models.Model):
    """
    An endpoint that is hit whenever Slackchat objects
    are created or updated.

    Used to signal reserialization should happen for
    a slackchat renderer.
    """
    endpoint = models.URLField(unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.endpoint
