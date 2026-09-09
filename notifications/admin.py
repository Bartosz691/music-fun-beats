from django.contrib import admin

from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'notification_type',
        'order',
        'is_read',
        'created_at',
    )

    list_filter = (
        'notification_type',
        'is_read',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'message',
        'order__payment_code',
    )

    readonly_fields = (
        'created_at',
    )

    list_select_related = (
        'user',
        'order',
    )

    date_hierarchy = 'created_at'

    ordering = (
        '-created_at',
    )