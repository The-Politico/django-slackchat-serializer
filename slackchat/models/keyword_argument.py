from django.db import models


class KeywordArgument(models.Model):
    """
    Replies to messages may contain key: value data.

    Used to create special handling for a message,
    e.g., tagging messages by category.
    """

    timestamp = models.DateTimeField(unique=True)
    key = models.SlugField(max_length=30)
    value = models.TextField()
    message = models.ForeignKey(
        'Message', on_delete=models.CASCADE, related_name='kwargs')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return '{0}: {1}'.format(self.key, self.value)
