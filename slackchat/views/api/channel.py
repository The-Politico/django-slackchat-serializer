from rest_framework.views import APIView
from rest_framework.response import Response
from slackchat.serializers import ChannelCMSSerializer, ChannelSerializer
from slackchat.models import Channel, ChatType, User
from slackchat.celery import post_webhook_republish, post_webhook_unpublish
from slackchat.authentication import TokenAPIAuthentication


channelNotFound404 = Response(
    {"detail": "Channel not found. It may have been deleted."}, 404
)

typeNotFound404 = Response(
    {"detail": "Chat type not found. It may have been deleted."}, 404
)

userNotFound404 = Response(
    {"detail": "User not found. It may have been deleted."}, 404
)

notUnique400 = Response(
    {
        "detail": "This publish path is already being used. Change the path"
        + " or chat type and try again."
    },
    400,
)


class ChannelDeserializer(APIView):
    """
    View to handle data from CMS.
    """

    authentication_classes = (TokenAPIAuthentication,)
    permission_classes = ()

    @staticmethod
    def is_path_unique(pk, channel_path, type_path):
        chans = Channel.objects.filter(
            publish_path=channel_path
        ).select_related("chat_type")

        for chan in chans:
            if (
                str(pk) != str(chan.pk)
                and chan.chat_type.publish_path == type_path
            ):
                return False

        return True

    def handle_webhook(self, c):
        if c.published:
            post_webhook_republish.delay(
                ChannelSerializer(c).data, c.chat_type.name
            )
        else:
            post_webhook_unpublish.delay(
                ChannelSerializer(c).data, c.chat_type.name
            )

    def get(self, request, format=None):
        return Response(200)

    def post(self, request, format=None):
        """
        Add a new Channel.
        """
        data = request.data.copy()

        # Get chat type record
        try:
            ct = ChatType.objects.get(pk=data.pop("chat_type"))
            data["chat_type"] = ct
        except ChatType.DoesNotExist:
            return typeNotFound404

        if not self.is_path_unique(
            None, data["publish_path"], ct.publish_path
        ):
            return notUnique400

        # Get user record
        try:
            u = User.objects.get(pk=data.pop("owner"))
            data["owner"] = u
        except User.DoesNotExist:
            return userNotFound404

        c = Channel(**data)
        c.save()

        self.handle_webhook(c)

        return Response(
            {
                "text": "Channel saved.",
                "method": "POST",
                "saved": ChannelCMSSerializer(c).data,
            },
            200,
        )

    def patch(self, request, format=None):
        """
        Update an existing Channel
        """
        data = request.data.copy()

        # Get chat type record
        try:
            ct = ChatType.objects.get(id=data.pop("chat_type"))
            data["chat_type"] = ct
        except ChatType.DoesNotExist:
            return typeNotFound404

        if not self.is_path_unique(
            data["id"], data["publish_path"], ct.publish_path
        ):
            return notUnique400

        # Get channel record
        try:
            c = Channel.objects.get(id=data.pop("id"))
        except Channel.DoesNotExist:
            return channelNotFound404

        # Save new data
        for key, value in data.items():
            setattr(c, key, value)
        c.save()

        self.handle_webhook(c)

        return Response(
            {
                "text": "Channel saved.",
                "method": "PATCH",
                "saved": ChannelCMSSerializer(c).data,
            },
            200,
        )
