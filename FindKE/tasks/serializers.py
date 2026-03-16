from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'ide', 'user', 'title', 'description', 'priority', 'completed', 'created_at', 'updated_at')
        read_only_fields = ('id', 'ide', 'user', 'created_at', 'updated_at')