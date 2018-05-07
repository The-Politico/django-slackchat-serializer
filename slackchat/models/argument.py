from django.db import models


class Argument(models.Model):
    """
    A type of Reaction on a message that occurs
    when a specific emoji is applied.

    Actions are defined per ChatType.
    """
    name = models.SlugField(
        max_length=255,
        help_text="The name of the argument that will be attached to a \
         message.")
    character = models.CharField(max_length=100)
    chat_type = models.ForeignKey(
        'ChatType', on_delete=models.CASCADE)

    def __str__(self):
        return ':{0}: = {1} for chat type {2}'.format(
            self.character,
            self.name,
            self.chat_type
        )

    class Meta:
        unique_together = ('character', 'chat_type')
