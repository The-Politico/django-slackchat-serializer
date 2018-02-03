from django.db import models


class CustomMessageTemplate(models.Model):
    """
    Defines search parameters for finding custom messages
    and a template for how to serialize the message
    """

    name = models.CharField(max_length=255)
    custom_action = models.SlugField(max_length=255)
    search_string = models.CharField(max_length=255)
    chat_type = models.ForeignKey(
        'ChatType', on_delete=models.CASCADE)
    content_template = models.TextField()

    def __str__(self):
        return self.name
