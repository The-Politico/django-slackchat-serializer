from rest_framework import viewsets

from .models import Channel, ChatType
from .serializers import (ChannelListSerializer, ChannelSerializer,
                          ChatTypeSerializer)


class ChannelViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = "pk"
    authentication_classes = []
    permission_classes = []
    pagination_class = None
    throttle_classes = []

    def get_serializer_class(self):
        if hasattr(self, "action") and self.action == "list":
            return ChannelListSerializer
        return ChannelSerializer

    def get_queryset(self):
        queryset = Channel.objects.all()
        chat_type = self.request.query_params.get("chat_type", None)
        if chat_type:
            queryset = queryset.filter(chat_type__name=chat_type)
        return queryset


class ChatTypeViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ChatType.objects.all()
    serializer_class = ChatTypeSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = None
    throttle_classes = []
