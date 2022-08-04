from django.urls import path
from . import views

urlpatterns = [
    path("", views.ActivitiesView.as_view(), name="activities_view"),
    path("<int:event_id>", views.EventActivitiesView.as_view(), name="event_activities_view"),
]