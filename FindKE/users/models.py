from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


def user_avatar_path(instance, filename):
    """Generate upload path for user avatars."""
    ext = filename.split('.')[-1]
    filename = f'{instance.id}.{ext}'
    return f'avatars/{filename}'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    # Social network features
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    # Additional profile fields
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # Email verification
    email_verified = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['first_name', 'last_name'], name='name_idx'),
            models.Index(fields=['created_at'], name='user_created_idx'),
        ]

    def __str__(self):
        return self.username

    @property
    def follower_count(self):
        """Return the number of followers."""
        return self.followers.count()

    @property
    def following_count(self):
        """Return the number of users being followed."""
        return self.following.count()

    def follow(self, user):
        """Follow another user."""
        if user != self and not self.is_following(user):
            user.followers.add(self)
            return True
        return False

    def unfollow(self, user):
        """Unfollow a user."""
        if self.is_following(user):
            user.followers.remove(self)
            return True
        return False

    def is_following(self, user):
        """Check if this user is following another user."""
        return self.following.filter(id=user.id).exists()


class FriendRequest(models.Model):
    """Model for friend requests."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'friend_requests'
        unique_together = ('from_user', 'to_user')
        indexes = [
            models.Index(fields=['from_user', 'status'], name='fr_from_status_idx'),
            models.Index(fields=['to_user', 'status'], name='fr_to_status_idx'),
            models.Index(fields=['created_at'], name='fr_created_idx'),
        ]

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"


