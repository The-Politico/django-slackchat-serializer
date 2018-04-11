from django.contrib import admin

from .celery import post_webhook, post_webhook_republish, update_users
from .models import (Argument, Attachment, Channel, ChatType,
                     CustomContentTemplate, KeywordArgument, Message, Reaction,
                     User, Webhook)


class ChannelAdmin(admin.ModelAdmin):
    readonly_fields = ('api_id', 'team_id',)
    fieldsets = (
        (None, {
            'fields': ('api_id', 'team_id', 'chat_type', 'owner')
        }),
        ('Publishing info', {
            'fields': ('publish_path', 'publish_time', 'live')
        }),
        ('Page content', {
            'fields': ('title', 'introduction')
        }),
        ('SEO tags', {
            'fields': ('meta_title', 'meta_description', 'meta_image')
        })
    )
    list_display = (
        'slackchat',
        'published_link',
        'api_link',
        'slack_link',
        'live',
    )
    autocomplete_fields = ['owner']
    actions = [
        'request_chats_update',
        'request_chats_republish',
        'close_live_chats',
    ]

    def request_chats_update(self, request, queryset):
        for channel in queryset:
            post_webhook.delay(channel.id.hex, channel.chat_type.name)
        self.message_user(request, 'Requested channels update chat page!')

    def request_chats_republish(self, request, queryset):
        for channel in queryset:
            post_webhook_republish.delay(
                channel.id.hex, channel.chat_type.name)
        self.message_user(request, 'Requested channels republish chat page!')

    def close_live_chats(self, request, queryset):
        queryset.update(live=False)
        for channel in queryset:
            post_webhook.delay(channel.id.hex, channel.chat_type.name)
        self.message_user(
            request,
            'Closed live channels and requested they update chat page!')


class UserAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    actions = ['update_user_profiles']

    def update_user_profiles(self, request, queryset):
        update_users.delay([user.pk for user in queryset])
        self.message_user(request, 'Updated user profiles!')


class WebhookAdmin(admin.ModelAdmin):
    fields = ('endpoint', 'verified',)


admin.site.register(Argument)
admin.site.register(Attachment)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(CustomContentTemplate)
admin.site.register(Message)
admin.site.register(Reaction)
admin.site.register(KeywordArgument)
admin.site.register(ChatType)
admin.site.register(Webhook, WebhookAdmin)
