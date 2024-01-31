from django.urls import path
from . import views

urlpatterns = [
    path("user/register/", views.UserRegister.as_view(), name="register"),
]
