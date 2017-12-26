from django.conf.urls import include, url
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from .viewsets import ChannelViewset

router = routers.DefaultRouter()
router.register(r'channel', ChannelViewset)

schema_view = get_swagger_view(title='Slackchat API Docs')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/docs/', schema_view),
]
