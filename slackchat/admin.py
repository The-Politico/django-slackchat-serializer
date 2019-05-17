import json
from django.contrib import admin
from foreignform.mixins import ForeignFormAdminMixin

from .serializers import ChannelSerializer

from .celery import (
    post_webhook,
    post_webhook_republish,
    post_webhook_unpublish,
    update_users,
)
from .models import (
    Argument,
    Attachment,
    Channel,
    ChatType,
    CustomContentTemplate,
    KeywordArgument,
    Message,
    Reaction,
    User,
    Webhook,
)


class ChatTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name", "publish_path")}),
        (
            "Channel options",
            {"fields": ("render_to_html", "kwargs_in_threads")},
        ),
        (
            "Extra channel fields",
            {
                "fields": ("jsonSchema", "uiSchema"),
                "description": (
                    'See the documentation for <a href="'
                    'https://github.com/mozilla-services/react-jsonschema-form"'
                    ' target="_blank"> '
                    "react-jsonschema-form</a> to learn how to configure extra "
                    "fields for channels of this type."
                ),
            },
        ),
    )


class ChannelAdmin(ForeignFormAdminMixin, admin.ModelAdmin):
    foreignform_foreign_key = "chat_type"
    foreignform_field = "extras"
    readonly_fields = ("api_id", "team_id")
    fieldsets = (
        (None, {"fields": ("api_id", "team_id", "chat_type", "owner")}),
        (
            "Publishing info",
            {"fields": ("publish_path", "publish_time", "live")},
        ),
        ("Page content", {"fields": ("title", "introduction")}),
        (
            "SEO tags",
            {"fields": ("meta_title", "meta_description", "meta_image")},
        ),
        ("Extra channel fields", {"fields": ("extras",)}),
    )
    list_display = (
        "slackchat",
        "published_link",
        "api_link",
        "slack_link",
        "live",
    )
    autocomplete_fields = ["owner"]
    actions = [
        "request_chats_update",
        "request_chats_republish",
        "request_chats_unpublish",
        "close_live_chats",
    ]

    def request_chats_update(self, request, queryset):
        for channel in queryset:
            post_webhook.delay(channel.id.hex, channel.chat_type.name)
        self.message_user(request, "Requested channels update chat page!")

    def request_chats_republish(self, request, queryset):
        for channel in queryset:
            post_webhook_republish.delay(
                ChannelSerializer(channel).data, channel.chat_type.name
            )
        self.message_user(request, "Requested channels republish chat page!")

    def request_chats_unpublish(self, request, queryset):
        for channel in queryset:
            post_webhook_unpublish.delay(
                ChannelSerializer(channel).data, channel.chat_type.name
            )
        self.message_user(request, "Requested channels unpublish chat page!")

    def close_live_chats(self, request, queryset):
        queryset.update(live=False)
        for channel in queryset:
            post_webhook.delay(channel.id.hex, channel.chat_type.name)
        self.message_user(
            request,
            "Closed live channels and requested they update chat page!",
        )


class UserAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name"]
    actions = ["update_user_profiles"]

    def update_user_profiles(self, request, queryset):
        update_users.delay([user.pk for user in queryset])
        self.message_user(request, "Updated user profiles!")


class WebhookAdmin(admin.ModelAdmin):
    fields = ("endpoint", "verified")


class MessageAdmin(admin.ModelAdmin):
    actions = ["serialize"]

    def serialize(self, request, queryset):
        for msg in queryset:
            msg.serialize()
        self.message_user(request, "Messages have been reserialized")


admin.site.register(Argument)
admin.site.register(Attachment)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(CustomContentTemplate)
admin.site.register(Message, MessageAdmin)
admin.site.register(Reaction)
admin.site.register(KeywordArgument)
admin.site.register(ChatType, ChatTypeAdmin)
admin.site.register(Webhook, WebhookAdmin)
