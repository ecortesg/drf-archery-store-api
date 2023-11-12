import factory
from django.utils.text import slugify
from .models import Brand, Category, Product


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand
        django_get_or_create = ["name"]

    name = factory.Sequence(lambda n: f"Brand {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ["name"]

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker("paragraph", nb_sentences=10)
    price = factory.Faker("pydecimal", min_value=100, max_value=5000)
    category = factory.Iterator(Category.objects.all())
    brand = factory.Iterator(Brand.objects.all())
    image = None
