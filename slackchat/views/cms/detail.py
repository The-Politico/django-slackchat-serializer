import json
from django.views.generic import TemplateView
from slackchat.models import Channel, ChatType, User
from slackchat.serializers import (
    ChannelCMSSerializer,
    ChatTypeSerializer,
    UserCMSSerializer,
)
from django.shortcuts import get_object_or_404
from .base import CMSBase


class CMSDetail(CMSBase, TemplateView):
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["all_chat_types"] = CMSBase.prep_data_for_injection(
            ChatType.objects.all(), ChatTypeSerializer, many=True
        )

        if "api_id" in self.kwargs:
            context["active_page"] = "edit"
            channel = get_object_or_404(Channel, api_id=self.kwargs["api_id"])
            context["data"] = CMSBase.prep_data_for_injection(
                channel, ChannelCMSSerializer
            )
            context["chat_type"] = CMSBase.prep_data_for_injection(
                channel.chat_type, ChatTypeSerializer
            )
            context["user"] = CMSBase.prep_data_for_injection({}, None)
        else:
            context["active_page"] = "new"

            user = get_object_or_404(User, email=self.request.user)

            context["user"] = CMSBase.prep_data_for_injection(
                user, UserCMSSerializer
            )
            context["data"] = CMSBase.prep_data_for_injection({}, None)
            context["chat_type"] = CMSBase.prep_data_for_injection({}, None)

        return context
