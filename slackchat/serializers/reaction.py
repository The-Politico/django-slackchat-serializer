from rest_framework import serializers
from slackchat.models import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.api_id

    class Meta:
        model = Reaction
        fields = (
            'timestamp',
            'reaction',
            'user'
        )
