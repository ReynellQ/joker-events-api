from django.db import models



from events.models import Events
from participants.models import Participant
# Create your models here.

class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    lugar = models.TextField()
    fechaHoraInicio = models.DateTimeField()
    fechaHoraFin = models.DateTimeField()
    idEvent = models.ForeignKey(Events, on_delete=models.DO_NOTHING)

    class Meta():
        db_table = 'activity'

class ActivityInscription(models.Model):
    class Status(models.TextChoices):
        INSCRITO = "I"
        NO_INSCRITO = "NI"
    idActivity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING)
    idParticipant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    registerDate = models.DateTimeField()
    status = models.CharField(max_length = 2, choices=Status.choices)
    class Meta():
        db_table = 'activity_inscription'