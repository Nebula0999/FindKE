from django.db import models
import uuid


CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

class Task(models.Model):
    ide = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        indexes = [
            models.Index(fields=['user'], name='task_user_idx'),
            models.Index(fields=['priority'], name='task_priority_idx'),
            models.Index(fields=['completed'], name='task_completed_idx'),
            models.Index(fields=['created_at'], name='task_created_at_idx'),
        ]

    def __str__(self):
        return self.title
