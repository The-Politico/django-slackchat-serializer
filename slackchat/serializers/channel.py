import os

from django.utils import timezone
from rest_framework import serializers
from slackchat.models import Channel

from .message import MessageSerializer
from .user import UserSerializer


class ChannelSerializer(serializers.ModelSerializer):
    chat_type = serializers.SerializerMethodField()
    publish_path = serializers.SerializerMethodField()
    paths = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    introduction = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True)

    def get_chat_type(self, obj):
        return obj.chat_type.name

    def get_paths(self, obj):
        return {
            'channel': obj.publish_path,
            'chat_type': obj.chat_type.publish_path
        }

    def get_publish_path(self, obj):
        """
        publish_path joins the publish_paths for the chat type and the channel.
        """
        return os.path.join(
            obj.chat_type.publish_path,
            obj.publish_path.lstrip('/')
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
            "image": obj.meta_image
        }

    def get_introduction(self, obj):
        return obj.get_introduction()

    class Meta:
        model = Channel
        fields = (
            'id',
            'api_id',
            'chat_type',
            'title',
            'introduction',
            'meta',
            'paths',
            'publish_path',
            'publish_time',
            'live',
            'users',
            'messages',
            'timestamp',
        )


class ChannelListSerializer(serializers.ModelSerializer):
    chat_type = serializers.SerializerMethodField()

    def get_chat_type(self, obj):
        return obj.chat_type.name

    class Meta:
        model = Channel
        fields = (
            'id',
            'api_id',
            'chat_type',
        )
