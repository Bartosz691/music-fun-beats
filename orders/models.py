from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from products.models import Album


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Koszyk użytkownika {self.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'album'],
                name='unique_album_in_cart',
            ),
        ]

    def __str__(self):
        return (
            f'{self.album.title} x {self.quantity} '
            f'w koszyku {self.cart.user.username}'
        )

    @property
    def subtotal(self):
        return self.album.price * self.quantity


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Oczekujące'
        PAID = 'paid', 'Opłacone'
        PROCESSING = 'processing', 'W realizacji'
        SHIPPED = 'shipped', 'Wysłane'
        COMPLETED = 'completed', 'Zakończone'
        CANCELLED = 'cancelled', 'Anulowane'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders',
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    payment_code = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Zamówienie #{self.id} - {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.PROTECT,
        related_name='order_items',
    )

    album_title = models.CharField(
        max_length=200,
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    def __str__(self):
        return (
            f'{self.album_title} x {self.quantity} '
            f'- zamówienie #{self.order_id}'
        )

    @property
    def subtotal(self):
        return self.unit_price * self.quantity