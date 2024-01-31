from django.contrib import admin
from .models import Order, OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("uuid", "created_at", "email", "total")
    search_fields = ("uuid", "email")
    ordering = ("-created_at",)
    readonly_fields = (
        "checkout_session_id",
        "created_at",
        "updated_at",
    )


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("uuid", "order", "product", "price", "count")
    search_fields = ("uuid", "order__uuid", "product__name")
    ordering = ("-created_at",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
