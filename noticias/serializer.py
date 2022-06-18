from django.utils import timezone
from rest_framework import serializers

from django.utils.translation import gettext as _
from noticias.models import News
from django.contrib.auth.models import User
from users.models import Profile, Rol


class NewsSerializer(serializers.Serializer):
    """
        A serializer to display and create a News
    """
    text = "Noticia creada"
    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField(required=False, max_length=200)
    publishedAt = serializers.DateTimeField()
    createdBy = serializers.CharField()
    visible = serializers.BooleanField()

    def validate_publishedAt(self, value):
        if value > timezone.now():
            raise serializers.ValidationError(
                _("Date is incorrect."))

    def validate_createdBy(self, value):
        try:
            u = User.objects.get(username=value)
            if u.profile.rol != Rol.OP:
                raise serializers.ValidationError(
                    _("The creator isn't a operator."))
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User doesn't exists."))
        return value

    def create(self, data):
        u: User = User.objects.get(username=data.pop('createdBy'))
        return News.objects.create(createdBy=u, **data)


class NewsIDSerializer(NewsSerializer):
    """
        A serializer to display a News with ID
    """
    text = "Noticia actualizada"
    instance = None
    id = serializers.IntegerField()

    def validate_id(self, value):
        try:
            NewsIDSerializer.instance = News.objects.get(id=value)
        except News.DoesNotExist:
            raise serializers.ValidationError(_("The news doesn't exists."))
        return value

    def create(self,  data):
        NewsIDSerializer.instance.createdBy = User.objects.get(
            username=data.pop('createdBy'))
        for attr, value in data.items():
            setattr(NewsIDSerializer.instance, attr, value)

        NewsIDSerializer.instance.save()
        return NewsIDSerializer.instance
