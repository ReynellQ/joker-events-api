from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Events(models.Model):
    title = models.CharField(max_length=50)
    lugar = models.CharField(max_length=100)
    aforo = models.IntegerField()
    description = models.TextField()
    cost = models.DecimalField(default=0.0, max_digits=14, decimal_places=2)
    date = models.DateField()
    visible = models.BooleanField()
    image = models.CharField(max_length=200, blank=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    gmaps = models.CharField(max_length=100)
    disponible = models.IntegerField()
    contacto = models.CharField(max_length = 100, default="")
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    createdAt = models.DateField(),
    visible = models.BooleanField(default=True)
    class Meta():
        db_table = 'events'
        order_with_respect_to = 'date'

class MediaEvents(models.Model):
    id_event = models.ForeignKey(
        'Events',
        on_delete=models.CASCADE
    )
    media = models.CharField(max_length=200)
    class Meta():
        db_table = 'media_events'