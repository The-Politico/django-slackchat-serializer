from django.conf.urls import include, url
from rest_framework import routers

from .viewsets import ChannelViewset
from .views import DRFDocsCustomView

router = routers.DefaultRouter()
router.register(r'channel', ChannelViewset)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/docs/', DRFDocsCustomView.as_view(),
        name="slackchat_api_docs"),
]