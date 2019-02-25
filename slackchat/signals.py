from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from slackchat.serializers import MessageSerializer

from .celery import (
    create_private_channel,
    post_webhook,
    update_users,
    verify_webhook,
)
from .models import (
    Attachment,
    Channel,
    KeywordArgument,
    Message,
    Reaction,
    User,
    Webhook,
)


@receiver(post_save, sender=Channel)
def save_channel(sender, instance, created, **kwargs):
    if created:
        create_private_channel.delay(instance.pk)


@receiver(post_save, sender=Webhook)
def save_webhook(sender, instance, **kwargs):
    verify_webhook.delay(instance.pk)


@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if created:
        update_users.delay([instance.pk])


@receiver(post_save, sender=Attachment)
@receiver(post_delete, sender=Attachment)
@receiver(post_save, sender=Reaction)
@receiver(post_delete, sender=Reaction)
@receiver(post_save, sender=KeywordArgument)
@receiver(post_delete, sender=KeywordArgument)
def reserialize_message(sender, instance, **kwargs):
    instance.message.serialize()


@receiver(post_save, sender=Message)
def notify_webhook(sender, instance, created, **kwargs):
    channel_id = instance.channel.id.hex
    message = MessageSerializer(instance=instance).data
    chat_type = instance.channel.chat_type.name

    if created:
        update_type = "message_created"
    else:
        update_type = "message_changed"

    transaction.on_commit(
        lambda: post_webhook.delay(channel_id, chat_type, update_type, message)
    )


@receiver(post_delete, sender=Message)
def notify_webhook_message_delete(sender, instance, **kwargs):
    channel_id = instance.channel.id.hex
    message = MessageSerializer(instance=instance).data
    chat_type = instance.channel.chat_type.name
    update_type = "message_deleted"

    transaction.on_commit(
        lambda: post_webhook.delay(channel_id, chat_type, update_type, message)
    )
