from datetime import datetime

from markslack import MarkSlack

from slackchat.models import Channel, Message, User

marker = MarkSlack()


def handle(id, event):
    if event.get('type', None) != 'message':
        return False

    subtype = event.get('subtype', None)
    if subtype:
        msg = {
            'user': event.get('previous_message').get('user'),
            'ts': event.get('previous_message').get('ts'),
            'text': event.get('message', {}).get('text', None)
        }
    else:
        msg = {
            'user': event.get('user'),
            'ts': event.get('ts'),
            'text': event.get('text')
        }

    try:
        channel = Channel.objects.get(
            id=event.get('channel')
        )
    except Exception as e:
        print('Not registered channel', event.get('channel'), e)
        return False

    user, created = User.objects.get_or_create(
        id=msg['user']
    )

    if subtype == 'message_deleted':
        Message.objects.get(
            channel=channel,
            timestamp=datetime.fromtimestamp(float(msg['ts'])),
            user=user,
        ).delete()
    else:
        Message.objects.update_or_create(
            channel=channel,
            timestamp=datetime.fromtimestamp(float(msg['ts'])),
            user=user,
            defaults={
                'text': marker.mark(msg['text'])
            }
        )
