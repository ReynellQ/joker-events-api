from rest_framework import serializers

from noticias.models import News
from django.contrib.auth.models import User
from users.models import Profile, Rol


class NewsSerializer(serializers.Serializer):
    """
        A serializer to display and create a News
    """
    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField(required=False, max_length=200)
    publishedAt = serializers.DateTimeField()
    createdBy = serializers.CharField()
    visible = serializers.BooleanField()

    def validate_createdBy(self, value):
        try:
            u = User.objects.get(username=value)
            if u.profile.rol != Rol.OP:
                raise serializers.ValidationError(
                    'El creador no es un operador')
        except User.DoesNotExist:
            raise serializers.ValidationError('Usuario no existe')
        return value

    def create(self, data):
        print(data)
        u: User = User.objects.get(username=data.pop('createdBy'))
        return News.objects.create(createdBy=u, **data)


class NewsIDSerializer(NewsSerializer):
    """
        A serializer to display a News with ID
    """
    id = serializers.IntegerField()
