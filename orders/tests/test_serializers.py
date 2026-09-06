from orders.serializers import AddToCartSerializer


def test_add_to_cart_serializer_accepts_valid_data():
    serializer = AddToCartSerializer(
        data={
            'album_id': 1,
            'quantity': 2,
        }
    )

    assert serializer.is_valid() is True
    assert serializer.validated_data['album_id'] == 1
    assert serializer.validated_data['quantity'] == 2


def test_add_to_cart_serializer_rejects_zero_quantity():
    serializer = AddToCartSerializer(
        data={
            'album_id': 1,
            'quantity': 0,
        }
    )

    assert serializer.is_valid() is False
    assert 'quantity' in serializer.errors