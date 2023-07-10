from rest_framework import serializers
from .models import Category, Product


class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
        )

class ProductSerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer()
    
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'get_absolute_url',
            'description',
            'price',
            'category',
            'get_image',
            'get_thumbnail',
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'get_absolute_url', 
            'products'
        )
        