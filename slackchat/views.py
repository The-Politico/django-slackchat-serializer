from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

from .handlers.messages import handle as handle_message
from .handlers.reactions import handle as handle_reaction

SLACK_VERIFICATION_TOKEN = getattr(
    settings,
    'SLACKCHAT_SLACK_VERIFICATION_TOKEN',
    None
)


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

            if event.get('type') == 'message':
                handle_message(id, event)

            if event.get('type') == 'reaction_added':
                handle_reaction(id, event)

        return Response(status=status.HTTP_200_OK)


class SwaggerSchemaView(APIView):
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)
