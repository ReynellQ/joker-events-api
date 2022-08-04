from django.urls import path
from . import views

urlpatterns = [
    path("", views.ActivitiesView.as_view(), name="activities_view"),
]