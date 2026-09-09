import json

from products.models import Album, Artist, MusicFormat
import pytest
from django.test import AsyncClient
from rest_framework.test import APIClient

from orders.tests.factories import AlbumFactory
from asgiref.sync import sync_to_async
from django.db import connections

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
    
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_graphql_returns_album_with_async_request():
    artist = await Artist.objects.acreate(
        name='Async GraphQL Artist',
    )

    music_format = await MusicFormat.objects.acreate(
        name='Async Vinyl',
    )

    album = await Album.objects.acreate(
        title='Async GraphQL Album',
        artist=artist,
        music_format=music_format,
        release_year=2026,
        price='49.99',
        stock=7,
        is_active=True,
    )

    client = AsyncClient()

    query = """
    query {
      albums {
        id
        title
        stock
      }
    }
    """

    response = await client.post(
        '/graphql/',
        data=json.dumps({
            'query': query,
        }),
        content_type='application/json',
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data.get('errors') is None

    albums = response_data['data']['albums']

    assert len(albums) == 1
    assert albums[0]['id'] == album.id
    assert albums[0]['title'] == 'Async GraphQL Album'
    assert albums[0]['stock'] == 7

    await sync_to_async(
        connections.close_all,
        thread_sensitive=True,
    )()