from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from markdown import markdown
from slackclient import SlackClient

TOKEN = getattr(settings, 'SLACKCHAT_SLACK_API_TOKEN', None)


class User(models.Model):
    """
    A Slack user that participates in a channel.
    """

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
    """
    A type of Slack chat
    """

    name = models.CharField(max_length=255)
    render_to_html = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Channel(models.Model):
    """
    A Slack channel that facilitates a live chat
    """

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
    """
    A role, e.g. moderator, that is attached to a chat type.
    """

    name = models.CharField(max_length=255)
    chat_type = models.ForeignKey(ChatType, related_name="roles")

    def __str__(self):
        return self.name


class RoleAssignment(models.Model):
    """
    Assigns a user to a role for a particular channel.
    """
    assignment = models.ForeignKey(User, related_name='assignments')
    role = models.ForeignKey(Role, related_name='assignments')
    channel = models.ForeignKey(Channel, related_name='assignments')

    def __str__(self):
        return 'User {0} {1} assigned Role {2} for channel {3}'.format(
            self.assignment.first_name,
            self.assignment.last_name,
            self.role.name,
            self.channel.name
        )


class Message(models.Model):
    """
    A message inside of a Slack channel, assigned to a user.
    """

    timestamp = models.DateTimeField(unique=True)

    channel = models.ForeignKey(Channel, related_name='messages')
    user = models.ForeignKey(User, related_name='messages')
    text = models.TextField()

    def html(self):
        return mark_safe(markdown(self.text))

    def __str__(self):
        return str(self.html())


class Key(models.Model):
    """
    Attached through a message through a reply.
    Expected to be a <key: value> format.
    """

    timestamp = models.DateTimeField(unique=True)
    # todo: custom class that is JSON serializable
    name = models.SlugField(max_length=30)
    value = models.TextField()
    message = models.ForeignKey(Message, related_name='keys')
    user = models.ForeignKey(User)

    def __str__(self):
        return '{0}: {1}'.format(self.key, self.value)


class Action(models.Model):
    """
    A type of Reaction on a message that occurs
    when a specific emoji is applied.

    Actions are defined per ChatType.
    """
    action_tag = models.SlugField(max_length=255)
    character = models.CharField(max_length=100)
    chat_type = models.ForeignKey(ChatType)
    role = models.ForeignKey(Role, null=True, blank=True)

    def __str__(self):
        return ':{0}: = {1} for chat type {2}'.format(
            self.character,
            self.action_tag,
            self.chat_type
        )


class Reaction(models.Model):
    """
    An emoji reaction to a message in Slack.
    """
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

    def __str__(self):
        return ':{0}:, reaction to "{1}"'.format(
            self.reaction,
            self.message.text
        )


class CustomMessageTemplate(models.Model):
    """
    Defines search parameters for finding custom messages
    and a template for how to serialize the message
    """

    name = models.CharField(max_length=255)
    custom_action = models.SlugField(max_length=255)
    search_string = models.CharField(max_length=255)
    regex = models.BooleanField(default=False)
    chat_type = models.ForeignKey(ChatType)
    content_template = models.TextField()

    def __str__(self):
        return self.name


class CustomMessage(models.Model):
    """
    An instance of a CustomMessageTemplate
    """
    message_template = models.ForeignKey(CustomMessageTemplate)
    message = models.OneToOneField(Message, related_name='custom_message')
    user = models.ForeignKey(User)
    content = models.TextField()

    def __str__(self):
        return self.message.text
