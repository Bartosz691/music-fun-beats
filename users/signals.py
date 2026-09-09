from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notification


User = get_user_model()


@receiver(post_save, sender=User)
def create_welcome_notification(sender, instance, created, **kwargs):
    if not created:
        return

    Notification.objects.create(
        user=instance,
        notification_type=Notification.NotificationType.WELCOME,
        message=(
            f'Welcome {instance.username}! '
            'Thank you for joining Music Fun Beats.'
        ),
    )