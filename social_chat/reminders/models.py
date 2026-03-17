from django.db import models
import uuid

class Reminder(models.Model):
    ide = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reminders')
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    remind_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reminders'
        indexes = [
            models.Index(fields=['user'], name='reminder_user_idx'),
            models.Index(fields=['task'], name='reminder_task_idx'),
            models.Index(fields=['remind_at'], name='reminder_remind_at_idx'),
            models.Index(fields=['created_at'], name='reminder_created_at_idx'),
        ]

    def __str__(self):
        return self.title
