import pytest
from rest_framework.test import APIClient

from orders.tests.factories import AlbumFactory


@pytest.mark.django_db
def test_graphql_returns_active_albums():
    client = APIClient()

    active_album = AlbumFactory(
        title='Active Album',
        is_active=True,
    )

    AlbumFactory(
        title='Inactive Album',
        is_active=False,
    )

    query = """
    query {
      albums {
        id
        title
        artistName
        price
      }
    }
    """

    response = client.post(
        '/graphql/',
        {'query': query},
        format='json',
    )

    assert response.status_code == 200

    data = response.json()['data']['albums']

    assert len(data) == 1
    assert data[0]['id'] == active_album.id
    assert data[0]['title'] == 'Active Album'


@pytest.mark.django_db
def test_graphql_returns_single_album():
    client = APIClient()

    album = AlbumFactory(
        title='GraphQL Album',
        stock=5,
    )

    query = f"""
    query {{
      album(id: {album.id}) {{
        id
        title
        stock
      }}
    }}
    """

    response = client.post(
        '/graphql/',
        {'query': query},
        format='json',
    )

    assert response.status_code == 200

    data = response.json()['data']['album']

    assert data['id'] == album.id
    assert data['title'] == 'GraphQL Album'
    assert data['stock'] == 5