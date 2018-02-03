from rest_framework import serializers
from slackchat.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'api_id',
            'first_name',
            'last_name',
            'image',
            'title'
        )
