import pytest

from notifications.models import Notification
from users.models import User


@pytest.mark.django_db
def test_welcome_notification_is_created_for_new_user():
    user = User.objects.create_user(
        username='welcome_user',
        email='welcome@example.com',
        password='test-password',
    )

    notification = Notification.objects.get(
        user=user,
        notification_type=Notification.NotificationType.WELCOME,
    )

    assert notification.is_read is False
    assert 'Music Fun Beats' in notification.message


@pytest.mark.django_db
def test_updating_user_does_not_create_another_welcome_notification():
    user = User.objects.create_user(
        username='update_user',
        email='update@example.com',
        password='test-password',
    )

    user.first_name = 'Updated'
    user.save()

    assert (
        Notification.objects.filter(
            user=user,
            notification_type=Notification.NotificationType.WELCOME,
        ).count()
        == 1
    )