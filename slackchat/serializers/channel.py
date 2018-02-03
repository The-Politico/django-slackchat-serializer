from rest_framework import serializers
from slackchat.models import Channel
from slackchat.serializers import MessageSerializer, UserSerializer


class ChannelSerializer(serializers.ModelSerializer):
    chat_type = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True)

    def get_chat_type(self, obj):
        return obj.chat_type.name

    def get_users(self, obj):
        users = []

        for message in obj.messages.all():
            serializer = UserSerializer(instance=message.user)
            if serializer.data not in users:
                users.append(serializer.data)

            for reaction in message.reactions.all():
                serializer = UserSerializer(instance=reaction.user)
                if serializer.data not in users:
                    users.append(serializer.data)

        return users

    class Meta:
        model = Channel
        fields = (
            'name',
            'title',
            'description',
            'keywords',
            'image',
            'chat_type',
            'users',
            'messages',
        )
