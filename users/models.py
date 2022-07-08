from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
# Create your models here.
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class Rol(models.TextChoices):
    ADMIN = 'admin'
    GER = 'gerente'
    OP = 'operador'
    PAR = 'participante'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=Rol.choices, blank=True)
    address = models.CharField(max_length=50, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=10, blank=True)

    def checkData(self):
        return self.getErrors() == []

    def getErrors(self):
        errors = []
        if self.rol not in Rol.values:
            errors.append("Rol inexistente")
        if len(self.user.password) < 8:
            errors.append("Password no permitida")
        if not re.fullmatch(regex, self.user.username):
            errors.append("Email invalido")
        return errors

    def __str__(self):
        return self.user.username + " " + self.rol

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
