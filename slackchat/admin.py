from django.contrib import admin

from .models import (Argument, Channel, ChatType, CustomContentTemplate,
                     KeywordArgument, Message, Reaction, User)


class ChannelAdmin(admin.ModelAdmin):
    readonly_fields = ('api_id',)
    fieldsets = (
        (None, {
            'fields': ('api_id', 'chat_type', 'owner')
        }),
        ('Page display', {
            'fields': ('image', 'title', 'introduction')
        }),
        ('Metadata', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        })
    )


admin.site.register(Argument)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(User)
admin.site.register(CustomContentTemplate)
admin.site.register(Message)
admin.site.register(Reaction)
admin.site.register(KeywordArgument)
admin.site.register(ChatType)
