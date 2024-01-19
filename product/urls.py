from django.urls import path
from . import views


urlpatterns = [
    path("home/", views.HomeView.as_view()),
    path("product/search/", views.ProductSearchView.as_view()),
    path(
        "product/<str:product_uuid>/",
        views.ProductDetailView.as_view(),
    ),
]
