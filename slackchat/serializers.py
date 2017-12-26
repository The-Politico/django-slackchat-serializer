from rest_framework import serializers

from .models import User, ChatType, Channel, Message, Reply, Reaction, MarkupContent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'image',
            'title'
        )


class ChatTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatType
        fields = ('name',)


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Message
        fields = (
            'timestamp',
            'user',
            'text'
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


class ActionSerializer(serializers.ModelSerializer):
    message_timestamp = serializers.SerializerMethodField()
    action_tag = serializers.SerializerMethodField()
    user = UserSerializer()

    def get_message_timestamp(self, obj):
        return obj.message.timestamp

    def get_action_tag(self, obj):
        return obj.action.action_tag

    class Meta:
        model = Reaction
        fields = (
            'timestamp',
            'message_timestamp',
            'action_tag',
            'user'
        )


class ReplySerializer(serializers.ModelSerializer):
    original_message_timestamp = serializers.SerializerMethodField()
    user = UserSerializer()

    def get_original_message_timestamp(self, obj):
        return obj.message.timestamp

    class Meta:
        model = Reply
        fields = (
            'timestamp',
            'original_message_timestamp',
            'user',
            'key',
            'value'
        )


class MarkupContentSerializer(serializers.ModelSerializer):
    original_message_timestamp = serializers.SerializerMethodField()
    user = UserSerializer()
    action_tag = serializers.SerializerMethodField()
    flow = serializers.SerializerMethodField()

    def get_original_message_timestamp(self, obj):
        return obj.message.timestamp

    def get_action_tag(self, obj):
        return obj.message_markup.action_tag

    def get_flow(self, obj):
        return obj.message_markup.flow

    class Meta:
        model = MarkupContent
        fields = (
            'action_tag',
            'flow',
            'original_message_timestamp',
            'user',
            'content'
        )


class ChannelSerializer(serializers.ModelSerializer):
    chat_type = ChatTypeSerializer()
    messages = MessageSerializer(many=True)
    reactions = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    markups = serializers.SerializerMethodField()

    def get_reactions(self, obj):
        reactions = []
        for message in obj.messages.all():
            for reaction in message.reactions.all():
                if not reaction.action:
                    serializer = ReactionSerializer(instance=reaction)
                    reactions.append(serializer.data)

        return reactions

    def get_actions(self, obj):
        actions = []
        for message in obj.messages.all():
            for reaction in message.reactions.all():
                if reaction.action:
                    serializer = ActionSerializer(instance=reaction)
                    actions.append(serializer.data)

        return actions

    def get_replies(self, obj):
        replies = []
        for message in obj.messages.all():
            for reply in message.replies.all():
                serializer = ReplySerializer(instance=reply)
                replies.append(serializer.data)

        return replies

    def get_markups(self, obj):
        markups = []
        for message in obj.messages.all():
            for markup in message.markups.all():
                serializer = MarkupContentSerializer(instance=markup)
                markups.append(serializer.data)

        return markups

    class Meta:
        model = Channel
        fields = (
            'name',
            'chat_type',
            'messages',
            'reactions',
            'actions',
            'replies',
            'markups'
        )
