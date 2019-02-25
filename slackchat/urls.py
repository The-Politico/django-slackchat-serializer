from django.urls import include, path
from rest_framework import routers

from .views import Events, CMSDetail, CMSList, ChannelDeserializer
from .viewsets import ChannelViewset, ChatTypeViewset

router = routers.DefaultRouter()
router.register(r"channels", ChannelViewset, base_name="slackchat-channel")
router.register(
    r"chat-types", ChatTypeViewset, base_name="slackchat-chat-types"
)

urlpatterns = [
    path("api/cms/", ChannelDeserializer.as_view(), name="cms-api"),
    path("api/", include(router.urls)),
    path("events/", Events.as_view()),
    path("cms/", CMSList.as_view(), name="cms-list"),
    path("cms/new/", CMSDetail.as_view(), name="cms-detail-new"),
    path("cms/<slug:id>/edit/", CMSDetail.as_view(), name="cms-detail-edit"),
]
