from django.db import models


class Role(models.Model):
    """
    A user role, e.g., moderator.

    Configured for each chat_type and used to provide
    special handling for messages from users with the
    role.
    """

    name = models.CharField(max_length=255)
    chat_type = models.ForeignKey(
        'ChatType', related_name="roles", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
