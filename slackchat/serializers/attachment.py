from rest_framework import serializers
from slackchat.models import Attachment

from .mixins import NoNonNullMixin


class AttachmentSerializer(NoNonNullMixin, serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = (
            'title',
            'title_link',
            'text',
            'service_name',
            'service_icon',
            'service_url',
            'image_url',
            'image_width',
            'image_height',
            'video_html',
            'video_html_width',
            'video_html_height',
            'thumb_url',
            'thumb_width',
            'thumb_height',
        )
