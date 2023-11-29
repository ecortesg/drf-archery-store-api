import factory
import datetime
import random
from django.utils.text import slugify
from .models import Category, Product
from decimal import Decimal


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ["name"]

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


def generate_discount():
    rand_num = random.random()
    # One third greater than 0
    if rand_num < 0.33:
        # Generate a random decimal between 0.1 and 0.5 with a step of 0.05
        return Decimal(round(random.uniform(0.1, 0.5) / 0.05) * 0.05)
    else:
        return Decimal(0)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker("paragraph", locale="la", nb_sentences=10)
    category = factory.SubFactory(CategoryFactory)
    price = factory.Faker("random_int", min=10, max=1000, step=5)
    discount = factory.LazyFunction(generate_discount)
    image = None
    release_date = factory.Faker(
        "date_between",
        start_date=datetime.date(2023, 1, 1),
        end_date=datetime.date(2023, 12, 31),
    )
