from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from slackchat.serializers import ChannelCMSSerializer
from slackchat.models import Channel, ChatType


class ChannelDeserializer(APIView):
    """
    View to handle data from CMS.
    """

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        return Response(200)

    def post(self, request, format=None):
        """
        Add a new Channel.
        """
        print("test")
        pass

    def patch(self, request, format=None):
        """
        Update an existing Channel
        """
        data = request.data.copy()

        # Get chat type record
        try:
            ct = ChatType.objects.get(id=data.pop("chat_type"))
            data["chat_type"] = ct
        except Channel.DoesNotExist:
            raise Http404()

        # Get channel record
        try:
            c = Channel.objects.get(id=data.pop("id"))
        except Channel.DoesNotExist:
            raise Http404()

        # Save new data
        print(data)
        for key, value in data.items():
            setattr(c, key, value)
        c.save()

        return Response(
            {
                "text": "Channel saved.",
                "method": "PATCH",
                "saved": ChannelCMSSerializer(c).data,
            },
            200,
        )
