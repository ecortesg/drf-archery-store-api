from django.db import models
from django.core.files import File
from io import BytesIO
from PIL import Image
import os
from django.conf import settings
from core.models import AbstractBaseModel
from drf_ecommerce_api.storage_backends import PublicMediaStorage
from django.core.files.storage import FileSystemStorage


def ImageStorage():
    if settings.USE_S3:
        return PublicMediaStorage()
    else:
        return FileSystemStorage()


class Brand(AbstractBaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


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
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.CASCADE)
    thumbnail = models.ImageField(storage=ImageStorage())

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.category.slug}/{self.slug}"

    def save(self, *args, **kwargs):
        if self.thumbnail:
            img = Image.open(self.thumbnail)
            max_width = 300
            max_height = 300
            img.thumbnail((max_width, max_height), Image.ANTIALIAS)

            thumb_io = BytesIO()
            img.save(thumb_io, format="JPEG", quality=85)
            thumbnail = File(thumb_io, name=f"thumb-{self.thumbnail.name}")
            self.thumbnail = thumbnail

        super().save(*args, **kwargs)


class ProductImage(AbstractBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(storage=ImageStorage())
