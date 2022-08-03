from rest_framework import serializers

from activities.models import Activity, ActivityInscription
from events.models import Events
from participants.models import Participant

class ActivitySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    lugar = serializers.CharField()
    fechaHoraInicio = serializers.DateTimeField()
    fechaHoraFin = serializers.DateTimeField()
    idEvent = serializers.IntegerField()

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

class Schedule(serializers.Serializer):
    participant = serializers.CharField()
    activities =  serializers.ListField(
        child=serializers.IntegerField()
    )
    def to_representation(self, instance : Participant):
        ret = {}
        ret["participant"] = instance.cedula
        activities = ActivityInscription.objects.filter(idParticipant = instance, status = ActivityInscription.Status.INSCRITO, idParticipant = algo)
        return ret