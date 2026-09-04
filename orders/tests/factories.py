from decimal import Decimal

import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from products.models import Album, Artist, MusicFormat


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(
        lambda number: f'user{number}'
    )

    email = factory.LazyAttribute(
        lambda user: f'{user.username}@example.com'
    )

    password = factory.LazyFunction(
        lambda: make_password('TestPassword123!')
    )


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Artist

    name = factory.Sequence(
        lambda number: f'Artist {number}'
    )


class MusicFormatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MusicFormat

    name = factory.Sequence(
        lambda number: f'Format {number}'
    )


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album

    title = factory.Sequence(
        lambda number: f'Album {number}'
    )

    artist = factory.SubFactory(ArtistFactory)
    music_format = factory.SubFactory(MusicFormatFactory)

    release_year = 2020
    price = Decimal('99.99')
    stock = 10
    is_active = True
    is_limited_edition = False
    purchase_limit = None