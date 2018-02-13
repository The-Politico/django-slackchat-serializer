from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Channel
from .serializers import ChannelSerializer


class ChannelViewset(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = 'pk'
    authentication_classes = []
    permission_classes = (IsAuthenticatedOrReadOnly,)
