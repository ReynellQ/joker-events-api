from django.utils import timezone
from rest_framework import serializers

from django.utils.translation import gettext as _
from noticias.models import News
from django.contrib.auth.models import User
from participants.models import EventInscription, Participant
from users.models import Profile, Rol
from events.models import Events

class UserSerializer(serializers.Serializer):
    """
        A serializer to display and create a Participant
    """
    nombre = serializers.CharField()
    apellido = serializers.CharField()
    email = serializers.EmailField()
    telefono = serializers.CharField()
    address = serializers.CharField()
    rol = serializers.CharField()
    ciudad = serializers.CharField()
    enabled = serializers.BooleanField()
    password = serializers.CharField(required = False)

    def to_representation(self, instance : User):
        ret = {}
        p : Profile = instance.profile
        ret['nombre'] = instance.first_name
        ret['apellido'] = instance.last_name
        ret['email'] = instance.username
        ret['telefono'] = p.telefono
        ret['address'] = p.address
        ret['rol'] = p.rol
        ret['ciudad'] = p.ciudad
        ret['enabled'] = instance.is_active

        return ret