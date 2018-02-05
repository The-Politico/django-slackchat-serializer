from celery import shared_task
from slackchat.conf import settings
from slackchat.models import Channel
from slackclient import SlackClient


@shared_task(acks_late=True)
def create_private_channel(pk):
    instance = Channel.objects.get(pk=pk)
    client = SlackClient(settings.SLACK_API_TOKEN)
    response = client.api_call(
        "conversations.create",
        name='slackchat-{}'.format(instance.id.hex[:10]),
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
