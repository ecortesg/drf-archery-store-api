from django.db import models
from product.models import Product
from core.models import AbstractBaseModel


class Order(AbstractBaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    street_1 = models.CharField(max_length=100)
    street_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    total_amount = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    stripe_session_id = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OrderProduct(AbstractBaseModel):
    order = models.ForeignKey(Order, related_name="products", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="ordered_product", on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id}"
