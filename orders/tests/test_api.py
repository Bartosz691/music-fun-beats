import pytest
from rest_framework.test import APIClient

from .factories import AlbumFactory, UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)

    return api_client, user


@pytest.mark.django_db
def test_add_album_to_cart_api(authenticated_client):
    client, user = authenticated_client
    album = AlbumFactory(stock=5)

    response = client.post(
        '/api/orders/cart/items/',
        {
            'album_id': album.id,
            'quantity': 2,
        },
        format='json',
    )

    assert response.status_code == 200
    assert response.data['album'] == album.title
    assert response.data['quantity'] == 2

    cart_item = user.cart.items.get(album=album)
    assert cart_item.quantity == 2


@pytest.mark.django_db
def test_add_album_above_stock_returns_conflict(
    authenticated_client,
):
    client, _ = authenticated_client
    album = AlbumFactory(stock=1)

    response = client.post(
        '/api/orders/cart/items/',
        {
            'album_id': album.id,
            'quantity': 2,
        },
        format='json',
    )

    assert response.status_code == 409
    assert 'Dostępna liczba sztuk' in response.data['detail']


@pytest.mark.django_db
def test_checkout_api_creates_order(authenticated_client):
    client, user = authenticated_client
    album = AlbumFactory(stock=5)

    client.post(
        '/api/orders/cart/items/',
        {
            'album_id': album.id,
            'quantity': 2,
        },
        format='json',
    )

    response = client.post(
        '/api/orders/checkout/',
        {},
        format='json',
    )

    assert response.status_code == 201
    assert response.data['status'] == 'pending'
    assert response.data['payment_code'].startswith('MFB-')

    assert user.orders.count() == 1
    assert user.cart.items.count() == 0