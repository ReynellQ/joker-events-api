from rest_framework import serializers

from activities.models import Activity, ActivityInscription
from events.models import Events
from participants.models import Participant

from django.forms.models import model_to_dict

class ActivitySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    lugar = serializers.CharField()
    fechaHoraInicio = serializers.DateTimeField()
    fechaHoraFin = serializers.DateTimeField()
    idEvent = serializers.IntegerField()

    def to_representation(self, instance : Activity):
        ret = {
                **model_to_dict(instance),
                'idEvent':instance.idEvent.id
            }
        return ret
    def validate_idEvent(self, value):
        try:
            e : Events = Events.objects.get( id = value )
            return value
        except Events.DoesNotExist as dne:
            raise serializers.ValidationError("The event doesnt exists")


    def create(self, validated_data):
        e : Events = Events.objects.get( id = validated_data.pop("idEvent") )
        a : Activity = Activity(**validated_data, idEvent = e)
        a.save()
        return a

class ActivityIDSerializer(ActivitySerializer):
    id = serializers.IntegerField()

    def update(self, instance, validated_data):
        
        return None
