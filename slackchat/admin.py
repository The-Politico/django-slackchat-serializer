from django.contrib import admin

from .models import Channel, Message, Reaction, User

admin.site.register(Channel)
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Reaction)
