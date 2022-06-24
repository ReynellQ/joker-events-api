from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Events(models.Model):
    title = models.CharField(max_length=50)
    lugar = models.CharField(max_length=100)
    aforo = models.IntegerField()
    description = models.TextField()
    precioBoleta = models.DecimalField(default=0.0, max_digits=14, decimal_places=2)
    visible = models.BooleanField()
    image = models.CharField(max_length=200, blank=True)
    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()
    gmaps = models.CharField(max_length=100)
    disponible = models.IntegerField()
    contacto = models.CharField(max_length = 100, default="")
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    createdAt = models.DateTimeField()
    visible = models.BooleanField(default=True)
    class Meta():
        db_table = 'events'
        order_with_respect_to = 'fechaInicio'

class MediaEvents(models.Model):
    id_event = models.ForeignKey(
        'Events',
        on_delete=models.CASCADE
    )
    element = models.IntegerField()
    media = models.CharField(max_length=200)
    class Meta():
        db_table = 'media_events'