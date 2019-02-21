import random
from django.conf import settings as project_settings


class Settings:
    pass


Settings.CMS_TOKEN = getattr(
    project_settings, "SLACKCHAT_CMS_TOKEN", "%032x" % random.getrandbits(128)
)

Settings.PUBLISH_ROOT = getattr(
    project_settings,
    "SLACKCHAT_PUBLISH_ROOT",
    "https://example.com/slackchat-root/",
)

Settings.SLACK_TEAM_ROOT = getattr(
    project_settings, "SLACKCHAT_TEAM_ROOT", "https://example.com/slack/"
)

Settings.MANAGERS = getattr(project_settings, "SLACKCHAT_MANAGERS", [])

Settings.DEFAULT_OWNER = getattr(
    project_settings, "SLACKCHAT_DEFAULT_OWNER", None
)

Settings.SLACK_VERIFICATION_TOKEN = getattr(
    project_settings, "SLACKCHAT_SLACK_VERIFICATION_TOKEN", None
)

Settings.SLACK_API_TOKEN = getattr(
    project_settings, "SLACKCHAT_SLACK_API_TOKEN", None
)

Settings.WEBHOOK_VERIFICATION_TOKEN = getattr(
    project_settings, "SLACK_WEBHOOK_VERIFICATION_TOKEN", "slackchat"
)

Settings.PUBLISH_ROOT = getattr(
    project_settings, "SLACKCHAT_PUBLISH_ROOT", None
)

Settings.MARKSLACK_USER_TEMPLATE = getattr(
    project_settings,
    "SLACK_MARKSLACK_USER_TEMPLATE",
    lambda user: '<span class="mention">{} {}</span>'.format(
        user.first_name, user.last_name
    ),
)

Settings.MARKSLACK_LINK_TEMPLATES = getattr(
    project_settings,
    "SLACK_MARKSLACK_LINK_TEMPLATES",
    {
        "twitter.com": '<blockquote class="twitter-tweet" data-lang="en"><a href="{}"></a></blockquote>'  # noqa
    },
)

Settings.MARKSLACK_IMAGE_TEMPLATE = getattr(
    project_settings, "SLACK_MARKSLACK_IMAGE_TEMPLATE", "[(image)]({})"
)


def default_user_image_upload_to(instance, filename):
    return "slackchat/users/{0}{1}/{2}".format(
        instance.first_name, instance.last_name, filename
    )


Settings.USER_IMAGE_UPLOAD_TO = getattr(
    project_settings,
    "SLACKCHAT_USER_IMAGE_UPLOAD_TO",
    default_user_image_upload_to,
)


settings = Settings
