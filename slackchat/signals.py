from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .celery import (create_private_channel, post_webhook, update_user,
                     verify_webhook)
from .models import (Attachment, Channel, KeywordArgument, Message, Reaction,
                     User, Webhook)


@receiver(post_save, sender=Channel)
def save_channel(sender, instance, created, **kwargs):
    if created:
        create_private_channel.delay(instance.pk)


@receiver(post_save, sender=Attachment)
@receiver(post_save, sender=Message)
@receiver(post_save, sender=Reaction)
@receiver(post_save, sender=KeywordArgument)
@receiver(post_delete, sender=Attachment)
@receiver(post_delete, sender=Message)
@receiver(post_delete, sender=Reaction)
@receiver(post_delete, sender=KeywordArgument)
def notify_webhook(sender, instance, **kwargs):
    if sender == Message:
        channel_id = instance.channel.id.hex
        chat_type = instance.channel.chat_type.name
    else:
        channel_id = instance.message.channel.id.hex
        chat_type = instance.message.channel.chat_type.name
    transaction.on_commit(lambda: post_webhook.delay(channel_id, chat_type))


@receiver(post_save, sender=Webhook)
def save_webhook(sender, instance, **kwargs):
    verify_webhook.delay(instance.pk)


@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if created:
        update_user.delay(instance.pk)
