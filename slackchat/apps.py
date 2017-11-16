from django.apps import AppConfig


class SlackchatConfig(AppConfig):
    name = 'slackchat'

    def ready(self):
        from slackchat import signals  # noqa
