from django.db import models
import uuid


class Notification(models.Model):
    """Model for user notifications."""
    TYPE_CHOICES = [
        ('like', 'Post Like'),
        ('comment', 'Post Comment'),
        ('follow', 'New Follower'),
        ('friend_request', 'Friend Request'),
        ('message', 'New Message'),
        ('mention', 'Mentioned in Post'),
        ('repost', 'Post Reposted'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField(max_length=500)

    # Optional related objects
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    conversation = models.ForeignKey('chat.Conversation', on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')

    # Status
    is_read = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at'], name='notif_recipient_idx'),
            models.Index(fields=['sender'], name='notif_sender_idx'),
            models.Index(fields=['notification_type'], name='notif_type_idx'),
        ]

    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient.username}"

    def mark_as_read(self):
        """Mark this notification as read."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
