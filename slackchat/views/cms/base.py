import json
from django.urls import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder
from slackchat.conf import settings as app_settings


class CMSBase(object):
    CMS_TOKEN = app_settings.CMS_TOKEN
    API_ROOT = reverse_lazy("cms-api")

    @staticmethod
    def prep_data_for_injection(queryset, serializer, many=False):
        if serializer:
            data = serializer(queryset, many=many).data
        else:
            data = {}

        return json.dumps(json.dumps(data, cls=DjangoJSONEncoder))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["CMS_TOKEN"] = self.CMS_TOKEN
        context["API_ROOT"] = self.API_ROOT
        return context
