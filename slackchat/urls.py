from django.urls import include, path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from .views import Events
from .viewsets import ChannelViewset

router = routers.DefaultRouter()
router.register(r'channel', ChannelViewset)

schema_view = get_swagger_view(title='Slackchat API Docs')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/docs/', schema_view),
    path('events/', Events.as_view()),
]
