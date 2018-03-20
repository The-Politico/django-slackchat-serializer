import uuid

import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from slackchat.conf import settings
from slackchat.models import User
from slacker import Slacker
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Retrieves users from Slack'

    def handle(self, *args, **options):
        SLACK = Slacker(settings.SLACK_API_TOKEN)
        slack_users = SLACK.users.list().body['members']
        for slack_user in tqdm(slack_users, desc='Users'):
            id = slack_user['id']
            profile = slack_user['profile']

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

            user, created = User.objects.update_or_create(
                api_id=id,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': profile.get('email', None),
                    'title': profile.get('title', 'Staff writer'),
                }
            )

            if created and profile.get('image_192', False):
                r = requests.get(profile.get('image_192'), stream=True)
                img = r.raw.read()
                user.image.save(
                    'profile-{}.jpg'.format(uuid.uuid4().hex[:10]),
                    ContentFile(img),
                    save=True
                )
            user.save()
