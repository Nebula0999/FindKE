from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post
from notifications.models import Notification


@receiver(m2m_changed, sender='users.User_followers')
def create_follow_notification(sender, instance, action, pk_set, **kwargs):
    """Create notification when a user is followed."""
    if action == 'post_add':
        for follower_id in pk_set:
            from users.models import User
            follower = User.objects.get(pk=follower_id)
            Notification.objects.create(
                recipient=instance,
                sender=follower,
                notification_type='follow',
                message=f"{follower.username} started following you"
            )
