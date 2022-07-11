from django.urls import path
from . import views

urlpatterns = [
    path("", views.ParticipantView.as_view(), name="participant_view"),
]