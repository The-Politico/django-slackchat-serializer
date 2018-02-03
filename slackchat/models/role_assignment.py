from django.db import models


class RoleAssignment(models.Model):
    """
    Assigns a user to a role for a particular slackchat channel.
    """
    assignment = models.ForeignKey(
        'User', related_name='assignments', on_delete=models.CASCADE)
    role = models.ForeignKey(
        'Role', related_name='assignments', on_delete=models.CASCADE)
    channel = models.ForeignKey(
        'Channel', related_name='assignments', on_delete=models.CASCADE)

    def __str__(self):
        return 'User {0} {1} assigned Role {2} for channel {3}'.format(
            self.assignment.first_name,
            self.assignment.last_name,
            self.role.name,
            self.channel.name
        )
