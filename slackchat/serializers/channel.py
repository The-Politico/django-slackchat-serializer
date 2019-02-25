import os

from django.utils import timezone
from rest_framework import serializers
from slackchat.models import Channel

from .message import MessageSerializer
from .user import UserSerializer


def blankify_nulls(val):
    if val is None:
        return ""

    return val


class ChannelSerializer(serializers.ModelSerializer):
    chat_type = serializers.SerializerMethodField()
    publish_path = serializers.SerializerMethodField()
    paths = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    introduction = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    def get_chat_type(self, obj):
        return obj.chat_type.name

    def get_paths(self, obj):
        return {
            "channel": obj.publish_path,
            "chat_type": obj.chat_type.publish_path,
        }

    def get_publish_path(self, obj):
        """
        publish_path joins the publish_paths for the chat type and the channel.
        """
        return os.path.join(
            obj.chat_type.publish_path, obj.publish_path.lstrip("/")
        )

    def get_users(self, obj):
        users = {}

        for message in obj.messages.all():
            user = message.user
            serializer = UserSerializer(instance=user)
            if user.api_id not in users:
                users[user.api_id] = serializer.data

            for reaction in message.reactions.all():
                serializer = UserSerializer(instance=reaction.user)
                if reaction.user.api_id not in users:
                    users[reaction.user.api_id] = serializer.data

        return users

    def get_timestamp(self, obj):
        return timezone.now()

    def get_meta(self, obj):
        return {
            "title": obj.meta_title,
            "description": obj.meta_description,
            "image": obj.meta_image,
        }

    def get_introduction(self, obj):
        return obj.get_introduction()

    def get_messages(self, obj):
        return [m.serialized for m in obj.messages.all()]

    class Meta:
        model = Channel
        fields = (
            "id",
            "api_id",
            "chat_type",
            "title",
            "introduction",
            "meta",
            "extras",
            "paths",
            "publish_path",
            "publish_time",
            "live",
            "users",
            "messages",
            "timestamp",
        )


class ChannelListSerializer(serializers.ModelSerializer):
    chat_type = serializers.SerializerMethodField()

    def get_chat_type(self, obj):
        return obj.chat_type.name

    class Meta:
        model = Channel
        fields = ("id", "api_id", "chat_type")


class ChannelCMSSerializer(serializers.ModelSerializer):
    chat_type = serializers.SerializerMethodField()
    introduction = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    publish_time = serializers.SerializerMethodField()

    def get_owner(self, obj):
        return obj.owner.id

    def get_chat_type(self, obj):
        return obj.chat_type.id

    def get_meta(self, obj):
        return {
            "title": blankify_nulls(obj.meta_title),
            "description": blankify_nulls(obj.meta_description),
            "image": blankify_nulls(obj.meta_image),
        }

    def get_introduction(self, obj):
        return blankify_nulls(obj.get_introduction())

    def get_title(self, obj):
        return blankify_nulls(obj.title)

    def get_publish_time(self, obj):
        return blankify_nulls(obj.publish_time)

    class Meta:
        model = Channel
        fields = (
            "id",
            "api_id",
            "chat_type",
            "owner",
            "title",
            "introduction",
            "meta",
            "extras",
            "publish_path",
            "publish_time",
            "published",
            "live",
        )
