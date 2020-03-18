from datetime import datetime
from django.utils.timezone import is_aware, make_aware

from django.core.exceptions import ObjectDoesNotExist
from markslack import MarkSlack

from slackchat.conf import settings
from slackchat.utils import log_event
from slackchat.exceptions import MessageNotFoundError, UserNotFoundError
from slackchat.models import Channel, KeywordArgument, Message, User


from .attachments import handle as handle_attachment

ignored_subtypes = ["group_join", "file_share", "group_archive"]


def strptimestamp(timestamp):
    date = datetime.fromtimestamp(float(timestamp))
    if not is_aware(date):
        date = make_aware(date)
    return date


def handle_removed(id, event):
    try:
        channel = Channel.objects.get(api_id=event.get("channel"))
    except ObjectDoesNotExist:
        log_event(200, "MESSAGE_IGNORED")
        return
    msg = {
        "user": event.get("previous_message").get("user"),
        "ts": event.get("previous_message").get("ts"),
        "text": event.get("message", {}).get("text", None),
    }
    user, created = User.objects.get_or_create(api_id=msg.get("user"))

    # If thread
    if not event.get("message", {}).get(
        "subtype"
    ) == "tombstone" and event.get("previous_message", {}).get("thread_ts"):
        if not channel.chat_type.kwargs_in_threads:
            return

        thread = event.get("previous_message")

        try:
            original_message = Message.objects.get(
                timestamp=strptimestamp(thread.get("thread_ts"))
            )
        except ObjectDoesNotExist:
            raise MessageNotFoundError(
                "{}".format(strptimestamp(thread.get("thread_ts")))
            )

        try:
            user = User.objects.get(api_id=thread.get("user"))
        except ObjectDoesNotExist:
            raise UserNotFoundError(thread.get("user"))

        try:
            kwarg = KeywordArgument.objects.get(
                timestamp=strptimestamp(thread.get("ts")),
                message=original_message,
                user=user,
            )
        except ObjectDoesNotExist:
            return

        log_event(200, "KWARG_DELETED")
        kwarg.delete()

    else:
        m = Message.objects.get(
            channel=channel, timestamp=strptimestamp(msg.get("ts")), user=user
        )
        log_event(200, "MESSAGE_DELETED")
        m.delete()


def handle(id, event):
    user_templates = {
        user.api_id: settings.MARKSLACK_USER_TEMPLATE(user)
        for user in User.objects.all()
    }

    marker = MarkSlack(
        user_templates=user_templates,
        link_templates=settings.MARKSLACK_LINK_TEMPLATES,
        image_template=settings.MARKSLACK_IMAGE_TEMPLATE,
    )

    try:
        channel = Channel.objects.get(api_id=event.get("channel"))
    except ObjectDoesNotExist:
        log_event(200, "MESSAGE_IGNORED")
        return

    subtype = event.get("subtype", None)
    if subtype in ignored_subtypes:
        return

    if subtype:
        msg = {
            "user": event.get("previous_message").get("user"),
            "ts": event.get("previous_message").get("ts"),
            "text": event.get("message", {}).get("text", None),
        }
    else:
        msg = {
            "user": event.get("user"),
            "ts": event.get("ts"),
            "text": event.get("text"),
        }

    user, created = User.objects.get_or_create(api_id=msg.get("user"))

    thread_ts = event.get("thread_ts", None) or event.get("message", {}).get(
        "thread_ts", None
    )
    # If thread
    if thread_ts and (
        event.get("parent_user_id", None)
        or event.get("message", {}).get("parent_user_id", None)
    ):
        if not channel.chat_type.kwargs_in_threads:
            return

        try:
            key, value = msg.get("text").split(": ", 1)
        except ValueError:
            # Don't handle threads that don't follow key-value pattern
            return

        try:
            original_message = Message.objects.get(
                timestamp=strptimestamp(thread_ts)
            )
        except ObjectDoesNotExist:
            raise MessageNotFoundError("{}".format(strptimestamp(thread_ts)))
        log_event(200, "KWARG_ADDED")
        KeywordArgument.objects.update_or_create(
            timestamp=strptimestamp(msg.get("ts")),
            message=original_message,
            user=user,
            defaults={"key": key, "value": value},
        )
    else:
        message, created = Message.objects.update_or_create(
            channel=channel,
            timestamp=strptimestamp(msg.get("ts")),
            user=user,
            defaults={"text": marker.mark(msg.get("text"))},
        )

        if created:
            log_event(200, "MESSAGE_CREATED")

        else:
            log_event(200, "MESSAGE_UPDATED")

        # Attachments
        attachments = event.get("message", {}).get("attachments")
        if attachments:
            for attachment in attachments:
                handle_attachment(message.pk, attachment)
