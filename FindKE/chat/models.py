from django.db import models
import uuid


def message_file_path(instance, filename):
    """Generate upload path for message files."""
    ext = filename.split('.')[-1]
    return f'chat/{instance.conversation.id}/{uuid.uuid4()}.{ext}'


class Conversation(models.Model):
    """Model for chat conversations."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField('users.User', related_name='conversations')
    is_group = models.BooleanField(default=False)
    group_name = models.CharField(max_length=255, blank=True)
    group_image = models.ImageField(upload_to='chat/groups/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at'], name='conv_updated_idx'),
            models.Index(fields=['is_group'], name='conv_group_idx'),
        ]

    def __str__(self):
        if self.is_group:
            return f"Group: {self.group_name or self.id}"
        participants = list(self.participants.all()[:2])
        if len(participants) == 2:
            return f"{participants[0].username} <-> {participants[1].username}"
        return f"Conversation {self.id}"

    @property
    def last_message(self):
        """Return the most recent message in this conversation."""
        return self.messages.first()


class Message(models.Model):
    """Model for chat messages."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(max_length=5000, blank=True)

    # File attachments
    file = models.FileField(upload_to=message_file_path, null=True, blank=True)
    file_type = models.CharField(max_length=50, blank=True)  # image, video, document, etc.

    # Message status
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['conversation', '-created_at'], name='msg_conv_created_idx'),
            models.Index(fields=['sender'], name='msg_sender_idx'),
        ]

    def __str__(self):
        content_preview = self.content[:50] if self.content else '[File]'
        return f"{self.sender.username}: {content_preview}..."


class MessageReadReceipt(models.Model):
    """Model for tracking message read receipts."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_receipts')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='message_receipts')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message_read_receipts'
        unique_together = ('message', 'user')
        indexes = [
            models.Index(fields=['message'], name='receipt_msg_idx'),
            models.Index(fields=['user'], name='receipt_user_idx'),
        ]

    def __str__(self):
        return f"{self.user.username} read message {self.message.id}"


class TypingStatus(models.Model):
    """Model for tracking typing status in conversations."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='typing_statuses')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='typing_in')
    is_typing = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'typing_statuses'
        unique_together = ('conversation', 'user')
        indexes = [
            models.Index(fields=['conversation', 'is_typing'], name='typing_conv_idx'),
        ]

    def __str__(self):
        status = "typing" if self.is_typing else "not typing"
        return f"{self.user.username} is {status} in {self.conversation.id}"
