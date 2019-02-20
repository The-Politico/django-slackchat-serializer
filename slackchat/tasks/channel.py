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
        name="slackchat-{}".format(instance.id.hex[:10]),
        is_private=True,
    )
    if response.get("ok", False):
        channel = response.get("channel")
        instance.api_id = channel.get("id")

        # Add team info
        response = client.api_call("team.info")
        if response.get("ok", False):
            team = response.get("team")
            instance.team_id = team.get("id")

        client.api_call(
            "groups.invite",
            channel=instance.api_id,
            user=instance.owner.api_id,
        )

        for manager in settings.MANAGERS:
            client.api_call(
                "groups.invite", channel=instance.api_id, user=manager
            )

    instance.save()
