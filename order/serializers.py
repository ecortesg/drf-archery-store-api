from rest_framework import serializers
from .models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ["product", "count"]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "country",
            "street_1",
            "street_2",
            "city",
            "state",
            "zip_code",
            "email",
            "phone_number",
            "stripe_session_id",
            "products",
        ]

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        order = Order.objects.create(**validated_data)

        for product in products_data:
            OrderProduct.objects.create(
                order=order, product=product.get("product"), count=product.get("count")
            )

        return order
