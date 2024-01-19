from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.pagination import StandardResultsSetPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Product, CarouselImage
from .serializers import ProductSerializer, HomeSerializer, ProductDetailSerializer


class HomeView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = HomeSerializer

    def get(self, request):
        carousel_images = CarouselImage.objects.all().order_by("order")
        new_arrivals = Product.objects.all().order_by("-release_date")[:18]
        best_sellers = Product.objects.all().order_by("release_date")[:18]
        sale_items = Product.objects.filter(discount__gt=0).order_by("release_date")[
            :18
        ]

        serializer = HomeSerializer(
            {
                "carousel_images": carousel_images,
                "new_arrivals": new_arrivals,
                "best_sellers": best_sellers,
                "sale_items": sale_items,
            },
            # Allows the serializer to build the full URL for the image path
            context={"request": request},
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductDetailSerializer

    def get(self, request, product_uuid):
        product = get_object_or_404(Product, uuid=product_uuid)
        related_products = Product.objects.exclude(uuid=product_uuid).order_by("?")[:6]

        serializer = ProductDetailSerializer(
            {
                "details": product,
                "related_products": related_products,
            },  # Allows the serializer to build the full URL for the image path
            context={"request": request},
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductSearchView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
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
