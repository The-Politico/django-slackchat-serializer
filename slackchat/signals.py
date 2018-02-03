import uuid

import requests

from django.db.models.signals import post_save
from django.dispatch import receiver
from slackchat.conf import settings
from slackclient import SlackClient

from .models import Channel, CustomMessage, Key, Message, Reaction, Webhook


@receiver(post_save, sender=Channel)
def create_private_channel(sender, instance, created, **kwargs):
    if created:
        instance.name = uuid.uuid4().hex[:10]
        client = SlackClient(settings.SLACK_API_TOKEN)
        response = client.api_call(
            "conversations.create",
            name='slackchat-{}'.format(instance.name),
            is_private=True
        )
        if response.get('ok', False):
            channel = response.get('channel')
            instance.api_id = channel.get('id')
            client.api_call(
                "groups.invite",
                channel=instance.api_id,
                user=instance.owner
            )
        instance.save()


@receiver(post_save, sender=Message)
@receiver(post_save, sender=Reaction)
@receiver(post_save, sender=Key)
@receiver(post_save, sender=CustomMessage)
def notify_webhook(sender, instance, **kwargs):
    if sender == Message:
        instance_id = instance.channel.id
    else:
        instance_id = instance.message.channel.id

    data = {
        'id': instance_id
    }
    for webhook in Webhook.objects.all():
        if webhook.verified:
            requests.post(webhook.endpoint, data=data)
