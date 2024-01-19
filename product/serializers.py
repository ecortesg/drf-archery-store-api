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
            "discount",
            "discounted_price",
            "category",
            "image",
            "get_absolute_url",
        )


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ("uuid", "name", "image")


class HomeSerializer(serializers.Serializer):
    carousel_images = CarouselImageSerializer(many=True)
    new_arrivals = ProductSerializer(many=True)
    best_sellers = ProductSerializer(many=True)
    sale_items = ProductSerializer(many=True)


class ProductDetailSerializer(serializers.Serializer):
    details = ProductSerializer()
    related_products = ProductSerializer(many=True)
