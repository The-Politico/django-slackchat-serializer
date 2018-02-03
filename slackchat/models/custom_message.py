from django.db import models


class CustomMessage(models.Model):
    """
    An instance of a CustomMessageTemplate.
    """
    message_template = models.ForeignKey(
        'CustomMessageTemplate', on_delete=models.CASCADE)
    message = models.OneToOneField(
        'Message', related_name='custom_message', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.message.text
