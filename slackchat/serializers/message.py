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
    attachments = serializers.SerializerMethodField()
    # attachments = AttachmentSerializer(many=True, read_only=True)

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

        custom_arg = obj.get_custom_arg()
        if custom_arg:
            args.append(custom_arg)

        return args

    def get_kwargs(self, obj):
        kwargs = {}

        custom_kwargs = obj.get_custom_kwargs()
        if custom_kwargs:
            kwargs = custom_kwargs

        for kwarg in obj.kwargs.all():
            kwargs[kwarg.key] = kwarg.value

        return kwargs

    def get_attachments(self, obj):
        attachments = []

        for attachment in obj.attachments.all():
            if attachment:
                serializer = AttachmentSerializer(instance=attachment)
                attachments.append(serializer.data)

        custom_attachment = obj.get_custom_attachment()
        if custom_attachment:
            attachments.append(custom_attachment)

        return attachments

    class Meta:
        model = Message
        fields = (
            "timestamp",
            "user",
            "content",
            "reactions",
            "attachments",
            "args",
            "kwargs",
        )
