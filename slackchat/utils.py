import logging
from slackchat.conf import settings

slack_logger = logging.getLogger(settings.SLACK_LOGGER)


def log_event(code, note):
    slack_logger.info("SLACKCHAT EVENT        {}        {}".format(code, note))
