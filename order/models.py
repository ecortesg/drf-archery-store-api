from django.db import models
from product.models import Product
from user.models import User
from core.models import AbstractBaseModel
from decimal import Decimal
from django.core.validators import MinValueValidator


class Order(AbstractBaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    street_1 = models.CharField(max_length=100)
    street_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    checkout_session_id = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return f"{self.uuid}"


class OrderProduct(AbstractBaseModel):
    order = models.ForeignKey(Order, related_name="products", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="ordered_product", on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = Decimal(self.product.discounted_price)
        super().save(*args, **kwargs)

    @property
    def total(self):
        return str(self.price * self.count)
