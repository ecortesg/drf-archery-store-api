from django.urls import path
from . import views


urlpatterns = [
    path("carousel-images/", views.CarouselImages.as_view()),
    path("products/new-arrivals/", views.ProductsNewArrivals.as_view()),
    path("products/best-sellers/", views.ProductsBestSellers.as_view()),
    path("products/on-sale/", views.ProductsOnSale.as_view()),
    path("products/search/", views.SearchProducts.as_view()),
    path(
        "product/<str:product_uuid>/",
        views.ProductDetail.as_view(),
    ),
    path(
        "product/<str:product_uuid>/related/",
        views.ProductRelated.as_view(),
    ),
]
