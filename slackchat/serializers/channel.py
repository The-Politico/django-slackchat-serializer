from rest_framework import serializers
from slackchat.models import Channel

from .message import MessageSerializer
from .user import UserSerializer


class ChannelSerializer(serializers.ModelSerializer):
    chat_type = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    introduction = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True)

    def get_chat_type(self, obj):
        return obj.chat_type.name

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

    def get_meta(self, obj):
        return {
            "title": obj.meta_title,
            "description": obj.meta_description,
            "keywords": obj.meta_keywords
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
            'image',
            'introduction',
            'meta',
            'publish_path',
            'users',
            'messages',
        )
