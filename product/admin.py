from django.contrib import admin
from .models import Category, Product, CarouselImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name")
    search_fields = ("uuid", "name")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name")
    search_fields = ("uuid", "name")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "order")
    search_fields = ("uuid", "name")
    ordering = ("order",)
    readonly_fields = ("created_at", "updated_at")
