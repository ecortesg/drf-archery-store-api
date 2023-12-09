from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator
from core.models import AbstractBaseModel
from drf_ecommerce_api.storage_backends import PublicMediaStorage
from decimal import Decimal
from drf_spectacular.utils import extend_schema_field


def ImageStorage():
    if settings.USE_S3:
        return PublicMediaStorage()
    else:
        return FileSystemStorage()


class Category(AbstractBaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.slug}"


class Product(AbstractBaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    discount = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    image = models.ImageField(storage=ImageStorage(), blank=True, null=True)
    release_date = models.DateField()

    @property
    @extend_schema_field(str)
    def discounted_price(self):
        if self.discount > 0:
            discounted_price = self.price * (1 - self.discount)
            rounded_price = round(discounted_price, 2)
            return str(rounded_price)
        return str(self.price)

    @extend_schema_field(str)
    def get_absolute_url(self):
        return f"/{self.category.slug}/{self.slug}/{self.uuid}/"

    def __str__(self):
        return self.name


class CarouselImage(AbstractBaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(storage=ImageStorage())
    order = models.PositiveSmallIntegerField()
