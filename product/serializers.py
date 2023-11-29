from rest_framework import serializers
from .models import Category, Product, CarouselImage


class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer()

    class Meta:
        model = Product
        fields = (
            "uuid",
            "name",
            "description",
            "price",
            "category",
            "image",
            "get_absolute_url",
        )


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ("uuid", "name", "image")
