from django.contrib import admin

from .models import (Argument, Attachment, Channel, ChatType,
                     CustomContentTemplate, KeywordArgument, Message, Reaction,
                     User, Webhook)


class ChannelAdmin(admin.ModelAdmin):
    readonly_fields = ('api_id',)
    fieldsets = (
        (None, {
            'fields': ('api_id', 'chat_type', 'owner')
        }),
        ('Publishing', {
            'fields': ('publish_path', 'publish_time', 'live')
        }),
        ('Display', {
            'fields': ('image', 'title', 'introduction')
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        })
    )
    list_display = ('slack_channel', 'published_link', 'live',)


class WebhookAdmin(admin.ModelAdmin):
    fields = ('endpoint', 'verified',)
    readonly_fields = ('verified',)


admin.site.register(Argument)
admin.site.register(Attachment)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(User)
admin.site.register(CustomContentTemplate)
admin.site.register(Message)
admin.site.register(Reaction)
admin.site.register(KeywordArgument)
admin.site.register(ChatType)
admin.site.register(Webhook, WebhookAdmin)
