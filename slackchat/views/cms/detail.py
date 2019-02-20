from django.views.generic import TemplateView
from slackchat.models import Channel, ChatType, User, Webhook
from slackchat.serializers import (
    ChannelCMSSerializer,
    ChatTypeSerializer,
    UserCMSSerializer,
    WebhookSerializer,
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

        if "id" in self.kwargs:
            context["active_page"] = "edit"

            context["data"] = CMSBase.prep_data_for_injection(
                get_object_or_404(Channel, pk=self.kwargs["id"]),
                ChannelCMSSerializer,
            )

            context["user"] = CMSBase.prep_data_for_injection({}, None)
        else:
            context["active_page"] = "new"

            context["user"] = CMSBase.prep_data_for_injection(
                get_object_or_404(User, email=self.request.user),
                UserCMSSerializer,
            )
            context["data"] = CMSBase.prep_data_for_injection({}, None)
            context["chat_type"] = CMSBase.prep_data_for_injection({}, None)

        return context
