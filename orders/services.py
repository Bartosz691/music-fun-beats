from django.db import transaction

from products.services import validate_album_purchase

from .models import Cart, CartItem


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