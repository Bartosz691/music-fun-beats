import pytest

from products.models import Album, Artist, MusicFormat
from products.tasks import check_low_stock


@pytest.mark.django_db
def test_check_low_stock_returns_only_active_low_stock_albums():
    artist = Artist.objects.create(name='Daft Punk')
    music_format = MusicFormat.objects.create(name='Vinyl')

    low_stock_album = Album.objects.create(
        title='Discovery',
        artist=artist,
        music_format=music_format,
        release_year=2001,
        price='99.99',
        stock=2,
        is_active=True,
    )

    Album.objects.create(
        title='Random Access Memories',
        artist=artist,
        music_format=music_format,
        release_year=2013,
        price='109.99',
        stock=10,
        is_active=True,
    )

    Album.objects.create(
        title='Inactive Album',
        artist=artist,
        music_format=music_format,
        release_year=2020,
        price='79.99',
        stock=1,
        is_active=False,
    )

    result = check_low_stock()

    assert result == [low_stock_album.id]