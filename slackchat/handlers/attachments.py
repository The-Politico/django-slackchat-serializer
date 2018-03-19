from slackchat.models import Attachment, Message


def handle(message_pk, attachment):
    # TODO: For now, we're not attaching unfurled tweets.
    # This gets handled by markslack.
    if attachment.get('service_name') == 'twitter':
        return
    data = {
        'title': attachment.get('title'),
        'title_link': attachment.get('title_link'),
        'text': attachment.get('text'),
        'service_name': attachment.get('service_name'),
        'service_icon': attachment.get('service_icon'),
        'service_url': attachment.get('service_url'),
        'image_url': attachment.get('image_url'),
        'image_width': attachment.get('image_width'),
        'image_height': attachment.get('image_height'),
        'video_html': attachment.get('video_html'),
        'video_html_width': attachment.get('video_html_width'),
        'video_html_height': attachment.get('video_html_height'),
        'thumb_url': attachment.get('thumb_url'),
        'thumb_width': attachment.get('thumb_width'),
        'thumb_height': attachment.get('thumb_height'),
    }
    if data.get('title_link') or data.get('image_url'):
        message = Message.objects.get(pk=message_pk)
        Attachment.objects.get_or_create(message=message, **data)
