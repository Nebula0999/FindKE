from django.contrib import admin
from .models import Conversation, Message, MessageReadReceipt, TypingStatus


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_group', 'group_name', 'created_at')
    list_filter = ('is_group', 'created_at')
    search_fields = ('group_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'conversation', 'content_preview', 'created_at')
    list_filter = ('created_at', 'is_edited', 'is_deleted')
    search_fields = ('sender__username', 'content')
    readonly_fields = ('created_at', 'updated_at')

    def content_preview(self, obj):
        if obj.content:
            return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
        return '[File attachment]'
    content_preview.short_description = 'Content'


@admin.register(MessageReadReceipt)
class MessageReadReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'user', 'read_at')
    list_filter = ('read_at',)
    search_fields = ('user__username',)


@admin.register(TypingStatus)
class TypingStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'user', 'is_typing', 'updated_at')
    list_filter = ('is_typing', 'updated_at')
    search_fields = ('user__username',)
