from slackchat.models import Channel, ChatType, User
from slackchat.serializers import (
    ChannelCMSSerializer,
    ChatTypeSerializer,
    UserCMSSerializer,
)
from slackchat.conf import settings
from django.shortcuts import get_object_or_404
from .base import CMSBase


class CMSDetail(CMSBase):
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

            try:
                user = User.objects.get(email=self.request.user)
            except User.DoesNotExist:
                user = get_object_or_404(User, api_id=settings.DEFAULT_OWNER)

            context["user"] = CMSBase.prep_data_for_injection(
                user,
                UserCMSSerializer,
            )
            context["data"] = CMSBase.prep_data_for_injection({}, None)
            context["chat_type"] = CMSBase.prep_data_for_injection({}, None)

        return context
