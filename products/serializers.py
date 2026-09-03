from datetime import date

from rest_framework import serializers

from .models import Album, Artist, Genre, Label, MusicFormat


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']


class MusicFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicFormat
        fields = ['id', 'name']


class AlbumSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(
        source='artist.name',
        read_only=True,
    )

    format_name = serializers.CharField(
        source='music_format.name',
        read_only=True,
    )

    class Meta:
        model = Album
        fields = [
            'id',
            'title',
            'artist',
            'artist_name',
            'genres',
            'label',
            'music_format',
            'format_name',
            'release_year',
            'price',
            'stock',
            'is_active',
            'is_limited_edition',
            'purchase_limit',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        instance = self.instance

        release_year = attrs.get(
            'release_year',
            getattr(instance, 'release_year', None),
        )

        price = attrs.get(
            'price',
            getattr(instance, 'price', None),
        )

        is_limited_edition = attrs.get(
            'is_limited_edition',
            getattr(instance, 'is_limited_edition', False),
        )

        purchase_limit = attrs.get(
            'purchase_limit',
            getattr(instance, 'purchase_limit', None),
        )

        errors = {}

        if release_year is not None and release_year > date.today().year:
            errors['release_year'] = (
                'Rok wydania albumu nie może być z przyszłości.'
            )

        if price is not None and price <= 0:
            errors['price'] = (
                'Cena albumu musi być większa od zera.'
            )

        if is_limited_edition and purchase_limit is None:
            errors['purchase_limit'] = (
                'Edycja limitowana musi posiadać limit zakupu.'
            )

        if not is_limited_edition and purchase_limit is not None:
            errors['purchase_limit'] = (
                'Limit zakupu można ustawić tylko dla edycji limitowanej.'
            )

        if errors:
            raise serializers.ValidationError(errors)

        return attrs