from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view(), name="users"),
    path("auth", views.Auth.as_view(), name="auth"),
]
