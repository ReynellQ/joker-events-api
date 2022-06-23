from this import s
from rest_framework import serializers


class EventSerializer(serializers):
    title = serializers.CharField(max_length=50)
    lugar = serializers.CharField(max_length=100)
    image = serializers.CharField(required=False, max_length=200)
    aforo = serializers.IntegerField()
    description = serializers.CharField()
    precioBoleta = serializers.DecimalField(
        default=0.0, max_digits=14, decimal_places=2)
    fechaInicio = serializers.DateField()
    fechaFin = serializers.DateField()
    gmaps = serializers.CharField(max_length=100)
    disponible = serializers.IntegerField()
    contacto = serializers.CharField(max_length = 100)
    resources: serializers.ListField(
        child=serializers.CharField(max_length=200)
    )
    createdBy = serializers.CharField( max_length=200)
    createdAt = serializers.DateField()
    visible = serializers.BooleanField()


class EventIDSerializer(EventSerializer):
    id = serializers.IntegerField()
