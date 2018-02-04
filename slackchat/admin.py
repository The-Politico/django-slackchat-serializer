from django.contrib import admin

from .models import (Argument, Channel, ChatType, CustomContentTemplate,
                     KeywordArgument, Message, Reaction, User)


class ChannelAdmin(admin.ModelAdmin):
    readonly_fields = ('api_id', 'name',)
    fields = ('api_id', 'name', 'owner', 'chat_type')


admin.site.register(Argument)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(User)
admin.site.register(CustomContentTemplate)
admin.site.register(Message)
admin.site.register(Reaction)
admin.site.register(KeywordArgument)
admin.site.register(ChatType)
