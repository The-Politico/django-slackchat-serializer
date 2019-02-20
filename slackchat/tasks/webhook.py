import re
import uuid
import json

import requests

from celery import shared_task
from slackchat.conf import settings
from slackchat.models import Webhook
from django.core.serializers.json import DjangoJSONEncoder


@shared_task(acks_late=True)
def post_webhook(channel_id, chat_type, update_type=None, message=None):
    data = {
        "token": settings.WEBHOOK_VERIFICATION_TOKEN,
        "type": "update_notification",
        "channel": channel_id,
        "chat_type": chat_type,
        "update_type": None,
        "message": None,
    }

    if update_type:
        data["update_type"] = update_type

    if message:
        data["message"] = message

    for webhook in Webhook.objects.all():
        if webhook.verified:
            requests.post(webhook.endpoint, json=data)


@shared_task(acks_late=True)
def post_webhook_republish(channel, chat_type):
    data = {
        "token": settings.WEBHOOK_VERIFICATION_TOKEN,
        "type": "republish_request",
        "channel": channel["id"],
        "channel_data": json.dumps(channel, cls=DjangoJSONEncoder),
        "chat_type": chat_type,
    }
    for webhook in Webhook.objects.all():
        if webhook.verified:
            requests.post(webhook.endpoint, json=data)


@shared_task(acks_late=True)
def post_webhook_unpublish(channel, chat_type):
    data = {
        "token": settings.WEBHOOK_VERIFICATION_TOKEN,
        "type": "unpublish_request",
        "channel": channel["id"],
        "channel_data": json.dumps(channel, cls=DjangoJSONEncoder),
        "chat_type": chat_type,
    }
    for webhook in Webhook.objects.all():
        if webhook.verified:
            requests.post(webhook.endpoint, json=data)


def clean_response(response):
    """ Cleans string quoting in response. """
    response = re.sub("^['\"]", "", response)
    response = re.sub("['\"]$", "", response)
    return response


@shared_task(acks_late=True)
def verify_webhook(pk):
    webhook = Webhook.objects.get(pk=pk)
    if not webhook.verified:
        challenge = uuid.uuid4().hex[:10]
        response = requests.post(
            webhook.endpoint,
            json={
                "token": settings.WEBHOOK_VERIFICATION_TOKEN,
                "type": "url_verification",
                "challenge": challenge,
            },
        )
        if response.status_code == requests.codes.ok:
            if clean_response(response.text) == challenge:
                webhook.verified = True
                webhook.save()
