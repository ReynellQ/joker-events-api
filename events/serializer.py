from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from users.models import Profile, Rol
from events.models import Events, MediaEvents
from django.forms.models import model_to_dict

class EventSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    lugar = serializers.CharField(max_length=100)
    image = serializers.CharField(required=False, max_length=200)
    aforo = serializers.IntegerField(min_value = 1) #Minimo 0, positivo
    description = serializers.CharField()
    precioBoleta = serializers.DecimalField(
        default=0.0, max_digits=14, decimal_places=2)
    fechaInicio = serializers.DateTimeField()
    fechaFin = serializers.DateTimeField()
    gmaps = serializers.CharField(max_length=100)
    disponible = serializers.IntegerField(required = False)
    contacto = serializers.CharField(max_length = 100)
    resources = serializers.ListField(
        child=serializers.CharField(max_length=200)
    )
    createdBy = serializers.CharField( max_length=200)
    createdAt = serializers.DateTimeField(default= timezone.now)
    visible = serializers.BooleanField()

    text = "Event created."
    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['fechaInicio'] > data['fechaFin']:
            raise serializers.ValidationError("End date must be after begin date")
        return data

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
        media : list = data.pop('resources')
        e: Events = Events.objects.create(createdBy= u, disponible = data["aforo"], **data)
        for i, data in enumerate(media):
            me : MediaEvents = MediaEvents.objects.create(id_event=e, element= i, media = data)
        return e

    def to_representation(self, instance):
        ret = {
                **model_to_dict(instance),
                'createdBy':instance.createdBy.email,
                'resources': list(map(lambda r : r.media, MediaEvents.objects.filter(id_event= instance.id)))
            }
        return ret


class EventIDSerializer(EventSerializer):
    """
        A serializer to display a News with ID
    """
    text = "Evento actualizado."
    instance = None
    id = serializers.IntegerField()

    def validate_id(self, value):
        try:
            EventIDSerializer.instance = Events.objects.get(id=value)
        except Events.DoesNotExist:
            raise serializers.ValidationError(_("The event doesn't exists."))
        return value

    def create(self,  data):
        EventIDSerializer.instance.createdBy = User.objects.get(
            username=data.pop('createdBy'))
        media : list = data.pop('resources')
        for attr, value in data.items():
            setattr(EventIDSerializer.instance, attr, value)
        MediaEvents.objects.filter(id_event = EventIDSerializer.instance).delete()
        for i, data in enumerate(media):
            me : MediaEvents = MediaEvents.objects.create(id_event=EventIDSerializer.instance, element= i, media = data)
        EventIDSerializer.instance.save()
        return EventIDSerializer.instance
    
    def to_representation(self, instance):
        ret = {
                **model_to_dict(instance),
                'createdBy':instance.createdBy.email,
                'resources': list(map(lambda r : r.media, MediaEvents.objects.filter(id_event= instance.id)))
            }
        ret.pop('id')
        return ret
    
