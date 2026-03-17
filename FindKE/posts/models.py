from django.db import models
import uuid


def post_image_path(instance, filename):
    """Generate upload path for post images."""
    ext = filename.split('.')[-1]
    return f'posts/{instance.user.id}/{uuid.uuid4()}.{ext}'


class Post(models.Model):
    """Model for user posts."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=5000)
    image = models.ImageField(upload_to=post_image_path, null=True, blank=True)

    # Repost functionality
    is_repost = models.BooleanField(default=False)
    original_post = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reposts'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at'], name='post_user_created_idx'),
            models.Index(fields=['-created_at'], name='post_created_idx'),
            models.Index(fields=['original_post'], name='post_original_idx'),
        ]

    def __str__(self):
        content_preview = self.content[:50]
        return f"{self.user.username}: {content_preview}..."

    @property
    def like_count(self):
        """Return the number of likes."""
        return self.likes.count()

    @property
    def comment_count(self):
        """Return the number of comments."""
        return self.comments.count()

    @property
    def repost_count(self):
        """Return the number of reposts."""
        return self.reposts.count()


class Like(models.Model):
    """Model for post likes."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['user'], name='like_user_idx'),
            models.Index(fields=['post'], name='like_post_idx'),
            models.Index(fields=['created_at'], name='like_created_idx'),
        ]

    def __str__(self):
        return f"{self.user.username} likes post {self.post.id}"


class Comment(models.Model):
    """Model for post comments."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=2000)

    # Reply functionality
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at'], name='comment_post_created_idx'),
            models.Index(fields=['user'], name='comment_user_idx'),
            models.Index(fields=['parent_comment'], name='comment_parent_idx'),
        ]

    def __str__(self):
        content_preview = self.content[:50]
        return f"{self.user.username}: {content_preview}..."
