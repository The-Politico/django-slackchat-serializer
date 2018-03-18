from django.contrib import admin

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


class UserAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']


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
