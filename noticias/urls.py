from django.urls import path
from . import views

urlpatterns = [
    path("", views.NewsView.as_view(), name="news_view"),
    path("public", views.Public_News, name="news_public_view"),
]
