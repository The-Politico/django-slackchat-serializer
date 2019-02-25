import json
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from slackchat.conf import settings as app_settings
from slackchat.authentication import secure


@secure
class CMSBase(TemplateView):
    @staticmethod
    def prep_data_for_injection(queryset, serializer, many=False):
        if serializer:
            data = serializer(queryset, many=many).data
        else:
            data = {}

        return json.dumps(json.dumps(data, cls=DjangoJSONEncoder))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PUBLISH_ROOT"] = app_settings.PUBLISH_ROOT
        context["SLACK_TEAM_ROOT"] = app_settings.SLACK_TEAM_ROOT
        context["CMS_TOKEN"] = app_settings.CMS_TOKEN
        context["API_ROOT"] = reverse_lazy("cms-api")
        return context
