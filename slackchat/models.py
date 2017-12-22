from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from markdown import markdown
from slackclient import SlackClient
from django.contrib.postgres.fields import JSONField

TOKEN = getattr(settings, 'SLACKCHAT_SLACK_API_TOKEN', None)


class User(models.Model):
    api_id = models.CharField(max_length=50)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField()
    title = models.CharField(max_length=255)

    def get_channel_assignments(self, channel):
        assignments = RoleAssignment.objects.filter(
            user=self,
            channel=channel
        )

        return assignments

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


class ChatType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Channel(models.Model):
    def fetch_slack_users():
        client = SlackClient(TOKEN)
        response = client.api_call("users.list")
        return [
            (m.get('id'), m.get('profile').get('email'))
            for m in response.get("members")
            if not m.get('deleted') and
            m.get('profile', {}).get('email', False)
        ]

    api_id = models.SlugField(
        max_length=10, null=True, blank=True, editable=False)

    name = models.CharField(
        max_length=150, blank=True, null=True, editable=False)
    owner = models.CharField(max_length=200, choices=fetch_slack_users())
    chat_type = models.ForeignKey(ChatType)

    def __str__(self):
        return 'slackchat-{}'.format(self.name)


class Role(models.Model):
    name = models.CharField(max_length=255)
    chat_type = models.ForeignKey(ChatType, related_name="roles")


class RoleAssignment(models.Model):
    assignment = models.ForeignKey(User, related_name='assignments')
    role = models.ForeignKey(Role, related_name='assignments')
    channel = models.ForeignKey(Channel, related_name='assignments')


class Message(models.Model):
    timestamp = models.DateTimeField(unique=True)

    channel = models.ForeignKey(Channel, related_name='messages')
    user = models.ForeignKey(User, related_name='messages')
    text = models.TextField()

    def html(self):
        return mark_safe(markdown(self.text))

    def __str__(self):
        return str(self.html())


class Reply(models.Model):
    timestamp = models.DateTimeField(unique=True)
    # todo: custom class that is JSON serializable
    key = models.SlugField(max_length=30)
    value = models.TextField()
    message = models.ForeignKey(Message, related_name='replies')
    user = models.ForeignKey(User)


class Action(models.Model):
    action_tag = models.SlugField(max_length=255)
    character = models.CharField(max_length=100)
    chat_type = models.ForeignKey(ChatType)
    role = models.ForeignKey(Role, null=True, blank=True)

    def __str__(self):
        return ':{1}: = {0} for chat type {2}'.format(
            self.action_tag,
            self.character,
            self.chat_type
        )


class Reaction(models.Model):
    timestamp = models.DateTimeField(unique=True)
    message = models.ForeignKey(Message, related_name='reactions')
    reaction = models.CharField(max_length=150)
    action = models.ForeignKey(Action, null=True, blank=True)
    user = models.ForeignKey(User)

    def valid_action_for_role(self):
        if self.action.role:
            channel = self.message.channel
            assignments = self.message.user.get_channel_assignments(channel)

            if self.action.role in assignments:
                return True
            else:
                return False
        else:
            return True


class MessageMarkup(models.Model):
    IN_FLOW = 'I'
    OUT_FLOW = 'O'
    BOTH = 'B'

    choices = (
        (IN_FLOW, 'In flow'),
        (OUT_FLOW, 'Out of flow'),
        (BOTH, 'Both')
    )

    name = models.SlugField(max_length=255)
    search_string = models.CharField(max_length=255)
    regex = models.BooleanField(default=False)
    chat_type = models.ForeignKey(ChatType)
    action_tag = models.SlugField(max_length=255)
    flow = models.CharField(
        max_length=1,
        choices=choices,
        default=IN_FLOW
    )
    content_template = JSONField()


class MarkupContent(models.Model):
    message_markup = models.ForeignKey(MessageMarkup)
    message = models.ForeignKey(Message)
    content = JSONField()
