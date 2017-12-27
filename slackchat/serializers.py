from rest_framework import serializers

from .models import User, Channel, Message, Reaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'image',
            'title'
        )


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    content = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    args = serializers.SerializerMethodField()
    kwargs = serializers.SerializerMethodField()

    def get_content(self, obj):
        if hasattr(obj, 'custom_message'):
            return obj.custom_message.content
        else:
            return obj.text

    def get_reactions(self, obj):
        reactions = []
        for reaction in obj.reactions.all():
            if not reaction.action:
                serializer = ReactionSerializer(instance=reaction)
                reactions.append(serializer.data)

        return reactions

    def get_args(self, obj):
        args = []

        for reaction in obj.reactions.all():
            if reaction.action:
                args.append(reaction.action.action_tag)

        if hasattr(obj, 'custom_message'):
            args.append(obj.custom_message.message_template.custom_action)

        return args

    def get_kwargs(self, obj):
        kwargs = {}

        for tag in obj.tags.all():
            kwargs[tag.key] = tag.value

        return kwargs

    class Meta:
        model = Message
        fields = (
            'timestamp',
            'user',
            'content',
            'reactions',
            'args',
            'kwargs',
        )


class ReactionSerializer(serializers.ModelSerializer):
    message_timestamp = serializers.SerializerMethodField()
    user = UserSerializer()

    def get_message_timestamp(self, obj):
        return obj.message.timestamp

    class Meta:
        model = Reaction
        fields = (
            'timestamp',
            'message_timestamp',
            'reaction',
            'user'
        )


class ChannelSerializer(serializers.ModelSerializer):
    chat_type = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True)

    def get_chat_type(self, obj):
        return obj.chat_type.name

    class Meta:
        model = Channel
        fields = (
            'name',
            'chat_type',
            'messages',
        )
