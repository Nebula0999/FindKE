from django.contrib import admin
from .models import Reminder

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'description', 'remind_at', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('remind_at', 'created_at')
    ordering = ('-created_at',)
