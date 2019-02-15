import json
from django.views.generic import TemplateView
from slackchat.models import Channel
from slackchat.serializers import ChannelListSerializer
from .base import CMSBase


class CMSList(CMSBase, TemplateView):
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        channels = Channel.objects.all()
        context["data"] = json.dumps(
            json.dumps(ChannelListSerializer(channels, many=True).data)
        )

        return context
