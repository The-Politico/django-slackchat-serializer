import uuid

import requests

from celery import shared_task
from django.core.files.base import ContentFile
from slackchat.conf import settings
from slackchat.models import User
from slacker import Slacker

SLACK = Slacker(settings.SLACK_API_TOKEN)


def get_slack_profile(user, users):
    """Return user profile from Slack."""
    for slack_user in users:
        if slack_user['id'] == user.api_id:
            return slack_user['profile']
    return None


@shared_task(acks_late=True)
def update_users(pks):
    users = SLACK.users.list().body['members']
    for pk in pks:
        user = User.objects.get(pk=pk)
        profile = get_slack_profile(user, users)

        real_name = profile.get('real_name', None)
        display_name = profile.get('display_name', None)
        try:
            first_name, last_name = real_name.split(' ', 1)
        except ValueError:
            try:
                first_name, last_name = display_name.split(' ', 1)
            except ValueError:
                first_name = real_name or display_name or ''
                last_name = ''

        user.first_name = first_name
        user.last_name = last_name
        user.title = profile.get('title', 'Staff writer')
        user.email = profile.get('email', None)

        if profile.get('image_192', False):
            r = requests.get(profile.get('image_192'), stream=True)
            img = r.raw.read()
            user.image.save(
                'profile-{}.jpg'.format(uuid.uuid4().hex[:10]),
                ContentFile(img),
                save=True
            )

        user.save()
