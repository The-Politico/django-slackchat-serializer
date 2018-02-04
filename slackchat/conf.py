from django.conf import settings as project_settings


class Settings:
    pass


Settings.SLACK_VERIFICATION_TOKEN = getattr(
    project_settings,
    'SLACKCHAT_SLACK_VERIFICATION_TOKEN',
    None
)

Settings.SLACK_API_TOKEN = getattr(
    project_settings,
    'SLACKCHAT_SLACK_API_TOKEN',
    None
)


def default_upload_to(instance, filename):
    return 'slackchat/users/{0}{1}/{2}'.format(
        instance.first_name,
        instance.last_name,
        filename,
    )


Settings.USER_IMAGE_UPLOAD_TO = getattr(
    project_settings,
    'SLACKCHAT_USER_IMAGE_UPLOAD_TO',
    default_upload_to
)

Settings.WEBHOOK_VERIFICATION_TOKEN = getattr(
    project_settings,
    'SLACK_WEBHOOK_VERIFICATION_TOKEN',
    'slackchat',
)


def default_user_template(user):
    return '<span class="mention">{} {}</span>'.format(
        user.first_name,
        user.last_name
    )


Settings.MARKSLACK_USER_TEMPLATE = getattr(
    project_settings,
    'SLACK_MARKSLACK_USER_TEMPLATE',
    default_user_template,
)

settings = Settings
