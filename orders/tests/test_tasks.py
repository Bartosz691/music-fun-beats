import pytest

from notifications.models import Notification
from orders.models import Order
from orders.tasks import process_order, send_order_notification
from users.models import User


@pytest.mark.django_db
def test_process_order_returns_order_data():
    user = User.objects.create_user(
        username='celery_test_user',
        email='celery@example.com',
        password='test-password',
    )

    order = Order.objects.create(
        user=user,
        total_price='99.99',
        payment_code='MFB-TEST1234',
    )

    result = process_order(order.id)

    assert result['order_id'] == order.id
    assert result['status'] == order.status


@pytest.mark.django_db
def test_send_order_notification_creates_notification():
    user = User.objects.create_user(
        username='notification_test_user',
        email='notification@example.com',
        password='test-password',
    )

    order = Order.objects.create(
        user=user,
        total_price='99.99',
        payment_code='MFB-NOTIFY12',
    )

    result = send_order_notification(order.id)

    notification = Notification.objects.get(
        user=user,
        order=order,
        notification_type=Notification.NotificationType.ORDER,
    )

    assert str(order.id) in result
    assert 'MFB-NOTIFY12' in result
    assert notification.user == user
    assert notification.order == order
    assert notification.is_read is False
    assert notification.message == result


@pytest.mark.django_db
def test_send_order_notification_does_not_create_duplicate():
    user = User.objects.create_user(
        username='duplicate_test_user',
        email='duplicate@example.com',
        password='test-password',
    )

    order = Order.objects.create(
        user=user,
        total_price='49.99',
        payment_code='MFB-DUPL1234',
    )

    send_order_notification(order.id)
    send_order_notification(order.id)

    notifications_count = Notification.objects.filter(
        user=user,
        order=order,
        notification_type=Notification.NotificationType.ORDER,
    ).count()

    assert notifications_count == 1