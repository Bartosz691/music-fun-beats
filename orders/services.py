from decimal import Decimal
from uuid import uuid4

from django.db import transaction

from products.models import Album
from products.services import validate_album_purchase

from .exceptions import EmptyCartError
from .models import Cart, CartItem, Order, OrderItem


@transaction.atomic
def add_to_cart(user, album, quantity=1):
    cart, _ = Cart.objects.get_or_create(user=user)

    cart_item = CartItem.objects.filter(
        cart=cart,
        album=album,
    ).first()

    if cart_item:
        new_quantity = cart_item.quantity + quantity
    else:
        new_quantity = quantity

    validate_album_purchase(
        album=album,
        quantity=new_quantity,
    )

    if cart_item:
        cart_item.quantity = new_quantity
        cart_item.save(update_fields=['quantity'])
    else:
        cart_item = CartItem.objects.create(
            cart=cart,
            album=album,
            quantity=quantity,
        )

    return cart_item


def generate_payment_code():
    return f'MFB-{uuid4().hex[:8].upper()}'


@transaction.atomic
def checkout(user):
    cart = (
        Cart.objects
        .select_for_update()
        .filter(user=user)
        .first()
    )

    if cart is None:
        raise EmptyCartError(
            'Użytkownik nie posiada koszyka.'
        )

    cart_items = list(
        CartItem.objects
        .select_for_update()
        .filter(cart=cart)
        .select_related('album')
    )

    if not cart_items:
        raise EmptyCartError(
            'Nie można złożyć zamówienia z pustego koszyka.'
        )

    validated_items = []

    for cart_item in cart_items:
        album = (
            Album.objects
            .select_for_update()
            .get(pk=cart_item.album_id)
        )

        validate_album_purchase(
            album=album,
            quantity=cart_item.quantity,
        )

        validated_items.append(
            (cart_item, album)
        )

    order = Order.objects.create(
        user=user,
        status=Order.Status.PENDING,
        payment_code=generate_payment_code(),
    )

    total_price = Decimal('0.00')

    for cart_item, album in validated_items:
        unit_price = album.price
        subtotal = unit_price * cart_item.quantity

        OrderItem.objects.create(
            order=order,
            album=album,
            album_title=album.title,
            quantity=cart_item.quantity,
            unit_price=unit_price,
        )

        album.stock -= cart_item.quantity
        album.save(update_fields=['stock'])

        total_price += subtotal

    order.total_price = total_price
    order.save(update_fields=['total_price'])

    CartItem.objects.filter(cart=cart).delete()

    return order