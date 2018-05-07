from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from markslack import MarkSlack
from slackchat.exceptions import MessageNotFoundError, ReactionNotFoundError
from slackchat.models import Argument, Channel, Message, Reaction, User

marker = MarkSlack()


def strptimestamp(timestamp):
    return datetime.fromtimestamp(float(timestamp))


def handle_removed(id, event):
    item = event.get('item')

    if item.get('type', None) != 'message':
        return

    item_user, created = User.objects.get_or_create(
        api_id=event.get('item_user')
    )

    user, created = User.objects.get_or_create(
        api_id=event.get('user')
    )

    try:
        channel = Channel.objects.get(
            api_id=item.get('channel')
        )
    except ObjectDoesNotExist:
        return

    try:
        message = Message.objects.get(
            timestamp=strptimestamp(item.get('ts')),
            channel=channel,
            user=item_user
        )
    except ObjectDoesNotExist:
        raise MessageNotFoundError('{} @ {} by {}'.format(
            channel,
            strptimestamp(item.get('ts')),
            item_user
        ))

    try:
        reaction = Reaction.objects.get(
            message=message,
            user=user,
            reaction=event.get('reaction'),
        )
    except ObjectDoesNotExist:
        raise ReactionNotFoundError('Can\'t find reaction.')

    reaction.delete()


def handle_added(id, event):
    item = event.get('item')

    if item.get('type', None) != 'message':
        return False

    item_user, created = User.objects.get_or_create(
        api_id=event.get('item_user')
    )

    try:
        channel = Channel.objects.get(
            api_id=item.get('channel')
        )
    except ObjectDoesNotExist:
        return

    try:
        message = Message.objects.get(
            timestamp=strptimestamp(item.get('ts')),
            channel=channel,
            user=item_user
        )
    except ObjectDoesNotExist:
        raise MessageNotFoundError('{} @ {} by {}'.format(
            channel,
            strptimestamp(item.get('ts')),
            item_user
        ))

    reaction_user, created = User.objects.get_or_create(
        api_id=event.get('user')
    )

    reaction_kwargs = {
        'timestamp': strptimestamp(event.get('event_ts')),
        'message': message,
        'reaction': event.get('reaction'),
        'user': reaction_user
    }

    try:
        argument = Argument.objects.get(
            character=event.get('reaction'),
            chat_type=channel.chat_type
        )
        reaction_kwargs['argument'] = argument
    except ObjectDoesNotExist:
        pass

    Reaction.objects.update_or_create(**reaction_kwargs)
