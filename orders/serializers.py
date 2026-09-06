from rest_framework import serializers

from .models import Cart, CartItem, Order, OrderItem


class AddToCartSerializer(serializers.Serializer):
    album_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CartItemSerializer(serializers.ModelSerializer):
    album_title = serializers.CharField(
        source='album.title',
        read_only=True,
    )

    unit_price = serializers.DecimalField(
        source='album.price',
        max_digits=8,
        decimal_places=2,
        read_only=True,
    )

    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'album',
            'album_title',
            'quantity',
            'unit_price',
            'subtotal',
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
            'created_at',
            'updated_at',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'album',
            'album_title',
            'quantity',
            'unit_price',
            'subtotal',
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'total_price',
            'payment_code',
            'items',
            'created_at',
            'updated_at',
        ]