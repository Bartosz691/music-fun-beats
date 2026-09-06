from django.urls import path

from .views import (
    AddToCartView,
    CartView,
    CheckoutView,
    OrderDetailView,
    OrderListView,
)


urlpatterns = [
    path(
        'cart/',
        CartView.as_view(),
        name='cart',
    ),
    path(
        'cart/items/',
        AddToCartView.as_view(),
        name='add_to_cart',
    ),
    path(
        'checkout/',
        CheckoutView.as_view(),
        name='checkout',
    ),
    path(
        '',
        OrderListView.as_view(),
        name='order_list',
    ),
    path(
        '<int:pk>/',
        OrderDetailView.as_view(),
        name='order_detail',
    ),
]