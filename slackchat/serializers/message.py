from rest_framework import serializers
from slackchat.models import Message

from .attachment import AttachmentSerializer
from .mixins import NoNonNullMixin
from .reaction import ReactionSerializer


class MessageSerializer(NoNonNullMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    args = serializers.SerializerMethodField()
    kwargs = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True, read_only=True)

    def get_user(self, obj):
        return obj.user.api_id

    def get_content(self, obj):
        if obj.channel.chat_type.render_to_html:
            return obj.html()
        else:
            return obj.get_content()

    def get_reactions(self, obj):
        reactions = []
        for reaction in obj.reactions.all():
            if not reaction.argument:
                serializer = ReactionSerializer(instance=reaction)
                reactions.append(serializer.data)

        return reactions

    def get_args(self, obj):
        args = []

        for reaction in obj.reactions.all():
            if reaction.argument:
                args.append(reaction.argument.name)

        template, match = obj.find_template_match()
        if match and template.argument_name:
            args.append(template.argument_name)

        return args

    def get_kwargs(self, obj):
        kwargs = {}

        for kwarg in obj.kwargs.all():
            kwargs[kwarg.key] = kwarg.value

        return kwargs

    class Meta:
        model = Message
        fields = (
            'timestamp',
            'user',
            'content',
            'reactions',
            'attachments',
            'args',
            'kwargs',
        )
