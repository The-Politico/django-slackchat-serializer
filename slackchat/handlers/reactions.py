from datetime import datetime

from markslack import MarkSlack

from slackchat.models import Action, Channel, Reaction, Message, User

marker = MarkSlack()


def handle(id, event):
    if event.get('type', None) != 'reaction_added':
        return False

    item = event.get('item')

    if item.get('type', None) != 'message':
        return False

    item_user_id = event.get('item_user')

    item_user, created = User.objects.get_or_create(
        api_id=item_user_id
    )

    try:
        channel = Channel.objects.get(
            api_id=item.get('channel')
        )
    except Exception as e:
        print('Not registered channel', item.get('channel'), e)
        return False

    try:
        message = Message.objects.get(
            timestamp=datetime.fromtimestamp(float(item.get('ts'))),
            channel=channel,
            user=item_user
        )
    except Exception as e:
        print('Unknown message', item.get('ts'), e)
        return False

    reaction_user, created = User.objects.get_or_create(
        api_id=event.get('user')
    )

    reaction_kwargs = {
        'timestamp': datetime.fromtimestamp(float(event.get('event_ts'))),
        'message': message,
        'reaction': event.get('reaction'),
        'user': reaction_user
    }
    
    try:
        action = Action.objects.get(character=event.get('reaction'))
        reaction_kwargs['action'] = action
    except:
        pass

    Reaction.objects.update_or_create(**reaction_kwargs)
