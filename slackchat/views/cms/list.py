from slackchat.models import Channel, ChatType
from slackchat.serializers import ChannelCMSSerializer, ChatTypeSerializer
from .base import CMSBase


class CMSList(CMSBase):
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["data"] = CMSBase.prep_data_for_injection(
            Channel.objects.order_by('publish_time', 'title'),
            ChannelCMSSerializer,
            many=True
        )

        context["all_chat_types"] = CMSBase.prep_data_for_injection(
            ChatType.objects.all(), ChatTypeSerializer, many=True
        )

        return context
