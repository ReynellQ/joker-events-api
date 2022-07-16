from django.db import models
from events.models import Events

# Create your models here.
from users.models import Profile

class Participant(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    cedula = models.CharField(max_length = 10, primary_key=True)
    birthdate = models.DateField()

    class Meta():
        db_table = 'participants'

class EventInscription(models.Model):
    class Status(models.TextChoices):
        INSCRITO = "I"
        CANCELADO = "C"
        DEVOLUCION = "D"
    idEvent = models.ForeignKey(Events, on_delete=models.DO_NOTHING)
    idParticipant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    status = models.CharField(max_length = 2, choices=Status.choices)
    registerDate = models.DateTimeField()
    class Meta():
        db_table = 'event_inscription'


class Devolution(models.Model):
    inscription = models.ForeignKey(EventInscription, on_delete=models.CASCADE)
    motivo = models.TextField()
    solicitudDate = models.DateTimeField()
    class Meta():
        db_table = 'devolution'