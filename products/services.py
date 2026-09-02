from .exceptions import (
    AlbumUnavailableError,
    InsufficientStockError,
    InvalidQuantityError,
    PurchaseLimitExceededError,
)


def validate_album_purchase(album, quantity):
    if quantity <= 0:
        raise InvalidQuantityError(
            'Liczba sztuk musi być większa od zera.'
        )

    if not album.is_active:
        raise AlbumUnavailableError(
            'Ten album nie jest obecnie dostępny w sprzedaży.'
        )

    if quantity > album.stock:
        raise InsufficientStockError(
            f'Dostępna liczba sztuk: {album.stock}.'
        )

    if (
        album.is_limited_edition
        and album.purchase_limit is not None
        and quantity > album.purchase_limit
    ):
        raise PurchaseLimitExceededError(
            f'Maksymalnie można kupić '
            f'{album.purchase_limit} szt. tego albumu.'
        )

    return True