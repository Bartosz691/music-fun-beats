from decimal import Decimal

import pytest

from orders.models import Order
from orders.services import add_to_cart, checkout
from products.exceptions import (
    InsufficientStockError,
    PurchaseLimitExceededError,
)

from .factories import AlbumFactory, UserFactory


@pytest.mark.django_db
def test_add_to_cart_increases_existing_quantity():
    user = UserFactory()
    album = AlbumFactory(stock=5)

    first_item = add_to_cart(
        user=user,
        album=album,
        quantity=2,
    )

    second_item = add_to_cart(
        user=user,
        album=album,
        quantity=2,
    )

    assert first_item.pk == second_item.pk
    assert second_item.quantity == 4
    assert user.cart.items.count() == 1


@pytest.mark.django_db
def test_add_to_cart_rejects_quantity_above_stock():
    user = UserFactory()
    album = AlbumFactory(stock=2)

    with pytest.raises(InsufficientStockError):
        add_to_cart(
            user=user,
            album=album,
            quantity=3,
        )


@pytest.mark.django_db
def test_limited_album_purchase_limit_is_enforced():
    user = UserFactory()

    album = AlbumFactory(
        stock=10,
        is_limited_edition=True,
        purchase_limit=2,
    )

    add_to_cart(
        user=user,
        album=album,
        quantity=2,
    )

    with pytest.raises(PurchaseLimitExceededError):
        add_to_cart(
            user=user,
            album=album,
            quantity=1,
        )


@pytest.mark.django_db
def test_checkout_creates_order_and_preserves_price():
    user = UserFactory()

    album = AlbumFactory(
        price=Decimal('99.99'),
        stock=5,
    )

    add_to_cart(
        user=user,
        album=album,
        quantity=2,
    )

    order = checkout(user)

    order_item = order.items.get()

    assert order.status == Order.Status.PENDING
    assert order.total_price == Decimal('199.98')
    assert order_item.unit_price == Decimal('99.99')
    assert order_item.quantity == 2

    album.refresh_from_db()

    assert album.stock == 3
    assert user.cart.items.count() == 0


@pytest.mark.django_db
def test_checkout_rechecks_stock_before_creating_order():
    user = UserFactory()
    album = AlbumFactory(stock=3)

    add_to_cart(
        user=user,
        album=album,
        quantity=3,
    )

    album.stock = 1
    album.save(update_fields=['stock'])

    with pytest.raises(InsufficientStockError):
        checkout(user)

    assert Order.objects.filter(user=user).count() == 0
    assert user.cart.items.get(album=album).quantity == 3