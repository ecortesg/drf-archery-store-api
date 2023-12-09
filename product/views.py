from rest_framework import generics
from .serializers import ProductSerializer, CarouselImageSerializer
from .models import Product, CarouselImage
from core.pagination import StandardResultsSetPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter


class ProductNewArrivals(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.all().order_by("-release_date")[:18]
        return products


class ProductBestSellers(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.all().order_by("release_date")[:18]
        return products


class ProductOnSale(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.filter(discount__gt=0).order_by("release_date")[:18]
        return products


class ProductSearch(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get("query")
        if query:
            return Product.objects.filter(name__icontains=query)

        return Product.objects.none()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="query",
                description="Search query to filter products by name.",
                type=str,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_uuid"

    def get_queryset(self):
        return Product.objects.filter(uuid=self.kwargs.get("product_uuid"))


class ProductRelated(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.exclude(uuid=self.kwargs.get("product_uuid")).order_by(
            "?"
        )[:6]


class CarouselImages(generics.ListAPIView):
    serializer_class = CarouselImageSerializer

    def get_queryset(self):
        return CarouselImage.objects.all().order_by("order")
