from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from posts.models import Like, Comment, Post
from users.models import FriendRequest


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """Create notification when a post is liked."""
    if created and instance.post.user != instance.user:
        Notification.objects.create(
            recipient=instance.post.user,
            sender=instance.user,
            notification_type='like',
            message=f"{instance.user.username} liked your post",
            post=instance.post
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when a comment is added to a post."""
    if created and instance.post.user != instance.user:
        Notification.objects.create(
            recipient=instance.post.user,
            sender=instance.user,
            notification_type='comment',
            message=f"{instance.user.username} commented on your post",
            post=instance.post,
            comment=instance
        )


@receiver(post_save, sender=Post)
def create_repost_notification(sender, instance, created, **kwargs):
    """Create notification when a post is reposted."""
    if created and instance.is_repost and instance.original_post:
        if instance.original_post.user != instance.user:
            Notification.objects.create(
                recipient=instance.original_post.user,
                sender=instance.user,
                notification_type='repost',
                message=f"{instance.user.username} reposted your post",
                post=instance.original_post
            )


@receiver(post_save, sender=FriendRequest)
def create_friend_request_notification(sender, instance, created, **kwargs):
    """Create notification when a friend request is sent."""
    if created and instance.status == 'pending':
        Notification.objects.create(
            recipient=instance.to_user,
            sender=instance.from_user,
            notification_type='friend_request',
            message=f"{instance.from_user.username} sent you a friend request"
        )
