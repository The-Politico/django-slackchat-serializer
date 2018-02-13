from rest_framework import serializers
from slackchat.models import ChatType


class ChatTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatType
        fields = '__all__'
