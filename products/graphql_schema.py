import strawberry

from .models import Album


@strawberry.type
class AlbumGraphQLType:
    id: int
    title: str
    artist_name: str
    genres: list[str]
    label_name: str | None
    format_name: str
    release_year: int
    price: str
    stock: int
    is_limited_edition: bool


def album_to_graphql(album):
    return AlbumGraphQLType(
        id=album.id,
        title=album.title,
        artist_name=album.artist.name,
        genres=[genre.name for genre in album.genres.all()],
        label_name=album.label.name if album.label else None,
        format_name=album.music_format.name,
        release_year=album.release_year,
        price=str(album.price),
        stock=album.stock,
        is_limited_edition=album.is_limited_edition,
    )


@strawberry.type
class Query:
    @strawberry.field
    def albums(self) -> list[AlbumGraphQLType]:
        albums = (
            Album.objects
            .filter(is_active=True)
            .select_related(
                'artist',
                'label',
                'music_format',
            )
            .prefetch_related('genres')
            .order_by('title')
        )

        return [
            album_to_graphql(album)
            for album in albums
        ]

    @strawberry.field
    def album(self, id: int) -> AlbumGraphQLType | None:
        album = (
            Album.objects
            .filter(
                pk=id,
                is_active=True,
            )
            .select_related(
                'artist',
                'label',
                'music_format',
            )
            .prefetch_related('genres')
            .first()
        )

        if album is None:
            return None

        return album_to_graphql(album)


schema = strawberry.Schema(query=Query)