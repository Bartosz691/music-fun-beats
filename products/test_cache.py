import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from products.models import Album, Artist, MusicFormat


@pytest.mark.django_db
def test_album_list_is_cached():
    cache.clear()

    artist = Artist.objects.create(name='Daft Punk')
    music_format = MusicFormat.objects.create(name='Vinyl')

    Album.objects.create(
        title='Discovery',
        artist=artist,
        music_format=music_format,
        release_year=2001,
        price='99.99',
        stock=5,
    )

    client = APIClient()

    first_response = client.get('/api/products/albums/')

    assert first_response.status_code == 200
    assert len(first_response.json()) == 1

    Album.objects.create(
        title='Random Access Memories',
        artist=artist,
        music_format=music_format,
        release_year=2013,
        price='109.99',
        stock=5,
    )

    second_response = client.get('/api/products/albums/')

    assert second_response.status_code == 200
    assert len(second_response.json()) == 1

    cache.clear()

    third_response = client.get('/api/products/albums/')

    assert third_response.status_code == 200
    assert len(third_response.json()) == 2