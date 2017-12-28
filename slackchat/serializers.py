from rest_framework import serializers

from .models import User, Channel, Message, Reaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'api_id',
            'first_name',
            'last_name',
            'image',
            'title'
        )


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    keys = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.api_id

    def get_content(self, obj):
        if hasattr(obj, 'custom_message'):
            return obj.custom_message.content
        else:
            if obj.channel.chat_type.render_to_html:
                return obj.html()
            else:
                return obj.text

    def get_reactions(self, obj):
        reactions = []
        for reaction in obj.reactions.all():
            if not reaction.action:
                serializer = ReactionSerializer(instance=reaction)
                reactions.append(serializer.data)

        return reactions

    def get_tags(self, obj):
        args = []

        for reaction in obj.reactions.all():
            if reaction.action:
                args.append(reaction.action.action_tag)

        if hasattr(obj, 'custom_message'):
            args.append(obj.custom_message.message_template.custom_action)

        return args

    def get_keys(self, obj):
        kwargs = {}

        for key in obj.keys.all():
            kwargs[key.name] = key.value

        return kwargs

    class Meta:
        model = Message
        fields = (
            'timestamp',
            'user',
            'content',
            'reactions',
            'tags',
            'keys',
        )


class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.api_id

    class Meta:
        model = Reaction
        fields = (
            'timestamp',
            'reaction',
            'user'
        )


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
            'chat_type',
            'users',
            'messages',
        )
