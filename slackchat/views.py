import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .handlers.messages import handle

SLACK_VERIFICATION_TOKEN = os.getenv('SLACK_VERIFICATION_TOKEN', None)


class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get('type') == 'url_verification':
            return Response(
                data=slack_message.get('challenge'),
                status=status.HTTP_200_OK
            )

        if 'event' in slack_message:
            id = slack_message.get('event_id')
            event = slack_message.get('event')
            handle(id, event)

        return Response(status=status.HTTP_200_OK)
