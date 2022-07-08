from django.utils import timezone
from rest_framework import serializers

from django.utils.translation import gettext as _
from noticias.models import News
from django.contrib.auth.models import User
from users.models import Profile, Rol


class ParticipantSerializer(serializers.Serializer):
    """
        A serializer to display and create a Participant
    """
    cedula =  serializers.CharField()
    nombre = serializers.CharField()
    apellidos = serializers.CharField()
    email = serializers.EmailField()
    celular = serializers.CharField()
    birthday = serializers.DateField()
    password = serializers.CharField()

    def create(self, data):
        u: User = User.objects.get(username=data.pop('createdBy'))
        return News.objects.create(createdBy=u, **data)
