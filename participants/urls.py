from django.urls import path
from . import views

urlpatterns = [
    path("participants", views.ParticipantView.as_view(), name="participant_view"),
    path("participants/<int:event_id>/", views.EventInscriptionView.as_view(), name="event_inscription_view"),
    path("devoluciones", views.DevolutionView.as_view(), name="event_inscription_view"),
]