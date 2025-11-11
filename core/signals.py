from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like, Follow, Message, Notification


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when a comment is added to a post."""
    if created and instance.user != instance.post.user:
        if not Notification.objects.filter(
            user=instance.post.user,
            from_user=instance.user,
            post=instance.post,
            notification_type='comment'  # ✅ Removed `comment=instance`
        ).exists():
            Notification.objects.create(
                user=instance.post.user,
                notification_type='comment',
                from_user=instance.user,
                post=instance.post,
                text=f"{instance.user.username} commented on your post."
            )


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """Create notification when a post is liked."""
    if created and instance.user != instance.post.user:
        if not Notification.objects.filter(
            user=instance.post.user, from_user=instance.user, post=instance.post, notification_type='like'
        ).exists():
            Notification.objects.create(
                user=instance.post.user,
                notification_type='like',
                from_user=instance.user,
                post=instance.post,
                text=f"{instance.user.username} liked your post."
            )

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    """Create notification when a user follows another user."""
    if created and instance.follower != instance.following:
        Notification.objects.get_or_create(
            user=instance.following,
            from_user=instance.follower,
            notification_type='follow',
            defaults={
                'text': f"{instance.follower.username} started following you."
            }
        )

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """Create notification when a message is received."""
    if created and instance.sender != instance.receiver:
        if not Notification.objects.filter(
            user=instance.receiver,
            from_user=instance.sender,
            notification_type='message'  # ✅ Removed `message=instance`
        ).exists():
            Notification.objects.create(
                user=instance.receiver,
                from_user=instance.sender,
                notification_type='message',
                text=f"New message from {instance.sender.username}"
            )

