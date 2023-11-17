from rest_framework import serializers
from .models import Category, Product


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
            "brand",
            "thumbnail",
            "get_absolute_url",
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ("uuid", "name", "get_absolute_url", "products")
