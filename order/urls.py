from django.urls import path
from order import views


urlpatterns = [path("order/checkout/", views.CheckoutView.as_view())]
