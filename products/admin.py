from django.contrib import admin

from .models import Album, Artist, Genre, Label, MusicFormat


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )


@admin.register(MusicFormat)
class MusicFormatAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'name',
    )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'artist',
        'music_format',
        'release_year',
        'price',
        'stock',
        'is_active',
        'is_limited_edition',
        'updated_at',
    )

    list_filter = (
        'is_active',
        'is_limited_edition',
        'music_format',
        'genres',
        'release_year',
    )

    search_fields = (
        'title',
        'artist__name',
        'label__name',
    )

    autocomplete_fields = (
        'artist',
        'label',
        'music_format',
    )

    filter_horizontal = (
        'genres',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    list_select_related = (
        'artist',
        'label',
        'music_format',
    )

    ordering = (
        'artist__name',
        'title',
    )