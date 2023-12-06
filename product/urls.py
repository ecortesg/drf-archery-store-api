from django.urls import path
from . import views


urlpatterns = [
    path("home/carousel-images/", views.CarouselImages.as_view()),
    path("product/new-arrivals/", views.ProductNewArrivals.as_view()),
    path("product/best-sellers/", views.ProductBestSellers.as_view()),
    path("product/on-sale/", views.ProductOnSale.as_view()),
    path("product/search/", views.ProductSearch.as_view()),
    path(
        "product/<str:product_uuid>/",
        views.ProductDetail.as_view(),
    ),
    path(
        "product/<str:product_uuid>/related/",
        views.ProductRelated.as_view(),
    ),
]
