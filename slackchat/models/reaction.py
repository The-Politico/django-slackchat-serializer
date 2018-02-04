from django.db import models


class Reaction(models.Model):
    """
    An emoji reaction to a message in Slack.
    """
    timestamp = models.DateTimeField(unique=True)
    message = models.ForeignKey(
        'Message', related_name='reactions', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=150)
    argument = models.ForeignKey(
        'Argument', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE)

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
