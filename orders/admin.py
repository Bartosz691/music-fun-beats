from django.contrib import admin

from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

    autocomplete_fields = (
        'album',
    )

    readonly_fields = (
        'added_at',
        'subtotal',
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'item_count',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    autocomplete_fields = (
        'user',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    inlines = (
        CartItemInline,
    )

    @admin.display(description='Items')
    def item_count(self, obj):
        return obj.items.count()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'album',
        'quantity',
        'subtotal',
        'added_at',
    )

    search_fields = (
        'cart__user__username',
        'cart__user__email',
        'album__title',
        'album__artist__name',
    )

    autocomplete_fields = (
        'album',
    )

    readonly_fields = (
        'added_at',
        'subtotal',
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False

    readonly_fields = (
        'album',
        'album_title',
        'quantity',
        'unit_price',
        'subtotal',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'total_price',
        'payment_code',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'payment_code',
    )

    autocomplete_fields = (
        'user',
    )

    readonly_fields = (
        'total_price',
        'payment_code',
        'created_at',
        'updated_at',
    )

    list_select_related = (
        'user',
    )

    date_hierarchy = 'created_at'

    inlines = (
        OrderItemInline,
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'album_title',
        'quantity',
        'unit_price',
        'subtotal',
    )

    search_fields = (
        'album_title',
        'order__payment_code',
        'order__user__username',
    )

    readonly_fields = (
        'album_title',
        'unit_price',
        'subtotal',
    )

    list_select_related = (
        'order',
        'album',
    )