from django.urls import path
from . import views

urlpatterns = [
    path("", views.ParticipantView.as_view(), name="participant_view"),
    path("<int:event_id>/", views.EventInscriptionView.as_view(), name="event_inscription_view"),
]