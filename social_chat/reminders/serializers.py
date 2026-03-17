from rest_framework import serializers

from .models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = (
            'id',
            'ide',
            'user',
            'task',
            'title',
            'description',
            'remind_at',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'ide', 'user', 'created_at', 'updated_at')
