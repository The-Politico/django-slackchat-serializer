import re

from datetime import datetime

from markslack import MarkSlack

from slackchat.models import (Channel, CustomMessageTemplate, CustomMessage,
                              Message, Key, User)

marker = MarkSlack()


def handle(id, event):
    print(event)
    if event.get('type', None) != 'message':
        return False

    subtype = event.get('subtype', None)

    if subtype in ['group_join', 'file_share']:
        return False

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
            api_id=event.get('channel')
        )
    except Exception as e:
        print('Not registered channel', event.get('channel'), e)
        return False

    user, created = User.objects.get_or_create(
        api_id=msg['user']
    )

    if subtype == 'message_deleted':
        Message.objects.get(
            channel=channel,
            timestamp=datetime.fromtimestamp(float(msg['ts'])),
            user=user,
        ).delete()
    elif event.get('thread_ts'):
        try:
            name = msg['text'].split(': ')[0]
            value = msg['text'].split(': ')[1]
        except Exception as e:
            print('Could not split reply into key/value pair', msg['text'], e)
            return False

        try:
            original_message = Message.objects.get(
                timestamp=datetime.fromtimestamp(float(event.get('thread_ts')))
            )
        except Exception as e:
            print('Unknown message replied to:', event.get('thread_ts'), e)
            return False

        Key.objects.update_or_create(
            timestamp=datetime.fromtimestamp(float(msg['ts'])),
            message=original_message,
            user=user,
            name=name,
            value=value
        )
    else:
        message, created = Message.objects.update_or_create(
            channel=channel,
            timestamp=datetime.fromtimestamp(float(msg['ts'])),
            user=user,
            defaults={
                'text': marker.mark(msg['text'])
            }
        )

        check_markup(message, user)


def check_markup(message, user):
    for template in CustomMessageTemplate.objects.all():
        m = re.search(template.search_string, message.text)
        if m:
            group_strings = [group for group in m.groups()]
            content = template.content_template.format(*group_strings)

            CustomMessage.objects.update_or_create(
                message=message,
                message_template=template,
                user=user,
                defaults={
                    'content': content
                }
            )
