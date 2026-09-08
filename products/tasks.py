import logging

from celery import shared_task

from products.models import Album


logger = logging.getLogger(__name__)


@shared_task
def check_low_stock(threshold=3):
    album_ids = list(
        Album.objects.filter(
            is_active=True,
            stock__lte=threshold,
        ).values_list(
            'id',
            flat=True,
        )
    )

    logger.info(
        'Low stock check found %s albums.',
        len(album_ids),
    )

    return album_ids