from django.contrib import admin

from .models import (Action, Channel, ChatType, CustomMessageTemplate,
                     Message, CustomMessage, Reaction, Key, User)


class ChannelAdmin(admin.ModelAdmin):
    readonly_fields = ('api_id', 'name',)
    fields = ('api_id', 'name', 'owner', 'chat_type')


admin.site.register(Action)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(User)
admin.site.register(CustomMessageTemplate)
admin.site.register(CustomMessage)
admin.site.register(Message)
admin.site.register(Reaction)
admin.site.register(Key)
admin.site.register(ChatType)
