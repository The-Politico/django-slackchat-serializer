from rest_framework import serializers
from slackchat.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'image',
            'title'
        )
