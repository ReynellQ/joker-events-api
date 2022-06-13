from django.db import models

# Create your models here.
class Events(models.Model):
    name = models.CharField(max_length=50)
    place = models.CharField(max_length=100)
    capacity = models.IntegerField()
    description = models.TextField()
    cost = models.DecimalField(default=0.0, max_digits=14, decimal_places=2)
    date = models.DateField()
    active = models.BooleanField()
    long = models.DecimalField(max_digits=8, decimal_places=3)
    lat = models.DecimalField(max_digits=8, decimal_places=3)
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