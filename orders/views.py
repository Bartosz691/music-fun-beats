from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.exceptions import (
    AlbumUnavailableError,
    InsufficientStockError,
    InvalidQuantityError,
    PurchaseLimitExceededError,
)
from products.models import Album

from .exceptions import EmptyCartError
from .models import Cart, Order
from .serializers import (
    AddToCartSerializer,
    CartSerializer,
    OrderSerializer,
)
from .services import add_to_cart, checkout


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(
            user=request.user,
        )

        serializer = CartSerializer(cart)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        try:
            album = Album.objects.get(
                pk=serializer.validated_data['album_id']
            )
        except Album.DoesNotExist:
            return Response(
                {'album_id': 'Album nie istnieje.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            item = add_to_cart(
                user=request.user,
                album=album,
                quantity=serializer.validated_data['quantity'],
            )

        except (
            AlbumUnavailableError,
            InsufficientStockError,
            PurchaseLimitExceededError,
        ) as exc:
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_409_CONFLICT,
            )

        except InvalidQuantityError as exc:
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'message': 'Produkt dodano do koszyka.',
                'album': item.album.title,
                'quantity': item.quantity,
            },
            status=status.HTTP_200_OK,
        )


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            order = checkout(request.user)

        except EmptyCartError as exc:
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except (
            AlbumUnavailableError,
            InsufficientStockError,
            PurchaseLimitExceededError,
        ) as exc:
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related('items')
            .order_by('-created_at')
        )


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related('items')
        )