from django.db import models


class Action(models.Model):
    """
    A type of Reaction on a message that occurs
    when a specific emoji is applied.

    Actions are defined per ChatType.
    """
    action_tag = models.SlugField(max_length=255)
    character = models.CharField(max_length=100)
    chat_type = models.ForeignKey(
        'ChatType', on_delete=models.CASCADE)
    role = models.ForeignKey(
        'Role', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return ':{0}: = {1} for chat type {2}'.format(
            self.character,
            self.action_tag,
            self.chat_type
        )
