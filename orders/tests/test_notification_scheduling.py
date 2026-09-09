import pytest

from orders.services import schedule_order_notification


@pytest.mark.django_db(transaction=True)
def test_schedule_order_notification_sends_celery_task(mocker):
    mocked_delay = mocker.patch(
        'orders.services.send_order_notification.delay'
    )

    schedule_order_notification(123)

    mocked_delay.assert_called_once_with(123)