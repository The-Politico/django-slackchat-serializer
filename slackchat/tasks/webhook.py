import uuid

import requests

from celery import shared_task
from slackchat.conf import settings
from slackchat.models import Webhook


@shared_task(acks_late=True)
def post_webhook(channel_id):
    data = {
        "token": settings.WEBHOOK_VERIFICATION_TOKEN,
        "type": "update_notification",
        "channel": channel_id,
    }
    for webhook in Webhook.objects.all():
        if webhook.verified:
            requests.post(webhook.endpoint, data=data)


@shared_task(acks_late=True)
def verify_webhook(pk):
    webhook = Webhook.objects.get(pk=pk)
    if not webhook.verified:
        challenge = uuid.uuid4().hex[:10]
        response = requests.post(webhook.endpoint, data={
            "token": settings.WEBHOOK_VERIFICATION_TOKEN,
            "type": "url_verification",
            "challenge": challenge,
        })
        if response.status_code == requests.codes.ok:
            if response.text == challenge:
                webhook.verified = True
                webhook.save()
