import requests
import uuid

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from slackclient import SlackClient

from .models import Channel, Message, Reaction, Key, CustomMessage

TOKEN = getattr(settings, 'SLACKCHAT_SLACK_API_TOKEN', None)
WEBHOOK = getattr(settings, 'SLACKCHAT_WEBHOOK', None)


@receiver(post_save, sender=Channel)
def create_private_channel(sender, instance, created, **kwargs):
    if created:
        instance.name = uuid.uuid4().hex[:10]
        client = SlackClient(TOKEN)
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
    if WEBHOOK:
        requests.post(WEBHOOK, data=data)
