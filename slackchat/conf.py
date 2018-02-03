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


settings = Settings
