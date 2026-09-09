import logging

from celery import shared_task

from notifications.models import Notification
from orders.models import Order


logger = logging.getLogger(__name__)


@shared_task
def process_order(order_id):
    order = Order.objects.get(pk=order_id)

    logger.info(
        'Processing order %s for user %s.',
        order.id,
        order.user_id,
    )

    return {
        'order_id': order.id,
        'status': order.status,
    }


@shared_task
def send_order_notification(order_id):
    order = Order.objects.select_related('user').get(
        pk=order_id
    )

    message = (
        f'Order {order.id} has been created. '
        f'Payment code: {order.payment_code}'
    )

    notification, created = Notification.objects.get_or_create(
        user=order.user,
        order=order,
        notification_type=Notification.NotificationType.ORDER,
        defaults={
            'message': message,
        },
    )

    if created:
        logger.info(
            'Order notification created for order %s.',
            order.id,
        )
    else:
        logger.info(
            'Order notification for order %s already exists.',
            order.id,
        )

    return notification.message