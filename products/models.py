from datetime import date

from django.core.exceptions import ValidationError
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class MusicFormat(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)

    artist = models.ForeignKey(
        Artist,
        on_delete=models.PROTECT,
        related_name='albums',
    )

    genres = models.ManyToManyField(
        Genre,
        related_name='albums',
    )

    label = models.ForeignKey(
        Label,
        on_delete=models.PROTECT,
        related_name='albums',
        null=True,
        blank=True,
    )

    music_format = models.ForeignKey(
        MusicFormat,
        on_delete=models.PROTECT,
        related_name='albums',
    )

    release_year = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    is_limited_edition = models.BooleanField(default=False)

    purchase_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'artist', 'music_format'],
                name='unique_album_artist_format',
            ),
        ]

    def clean(self):
        errors = {}

        if self.release_year > date.today().year:
            errors['release_year'] = (
                'Rok wydania albumu nie może być z przyszłości.'
            )

        if self.price <= 0:
            errors['price'] = (
                'Cena albumu musi być większa od zera.'
            )

        if self.is_limited_edition and self.purchase_limit is None:
            errors['purchase_limit'] = (
                'Edycja limitowana musi posiadać limit zakupu.'
            )

        if (
            self.is_limited_edition
            and self.purchase_limit is not None
            and self.purchase_limit < 1
        ):
            errors['purchase_limit'] = (
                'Limit zakupu musi wynosić co najmniej 1.'
            )

        if not self.is_limited_edition and self.purchase_limit is not None:
            errors['purchase_limit'] = (
                'Limit zakupu można ustawić tylko dla edycji limitowanej.'
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return (
            f'{self.artist} - {self.title} '
            f'({self.music_format})'
        )