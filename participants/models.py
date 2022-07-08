from django.db import models

# Create your models here.
from users.models import Profile

class Participant(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    cedula = models.CharField(max_length = 10, primary_key=True)
    birthdate = models.DateField()

    class Meta():
        db_table = 'participants'
