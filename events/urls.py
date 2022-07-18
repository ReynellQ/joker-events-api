from django.urls import path
from . import views

urlpatterns = [
    path("", views.EventView.as_view(), name="event_view"),
    path("public", views.Public_Events, name="events_public_view"),
]