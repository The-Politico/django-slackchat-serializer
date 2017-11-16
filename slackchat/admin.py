from django.contrib import admin

from .models import Channel, Message, Reaction, User


class ChannelAdmin(admin.ModelAdmin):
    readonly_fields = ('api_id', 'name',)
    fields = ('api_id', 'name', 'owner')


admin.site.register(Channel, ChannelAdmin)
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Reaction)
