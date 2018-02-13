from django.urls import include, path
from rest_framework import routers

from .views import Events
from .viewsets import ChannelViewset

router = routers.DefaultRouter()
router.register(r'channels', ChannelViewset, base_name='slackchat-channel')

urlpatterns = [
    path('api/', include(router.urls)),
    path('events/', Events.as_view()),
]
