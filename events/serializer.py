from this import s
from rest_framework import serializers


class EventSerializer(serializers):
    name = serializers.CharField(max_length=50)
    place = serializers.CharField(max_length=100)
    capacity = serializers.IntegerField()
    description = serializers.CharField()
    cost = serializers.DecimalField(
        default=0.0, max_digits=14, decimal_places=2)
    date = serializers.DateField()
    active = serializers.BooleanField()
    long = serializers.DecimalField(max_digits=8, decimal_places=3)
    lat = serializers.DecimalField(max_digits=8, decimal_places=3)


class EventIDSerializer(EventSerializer):
    id = serializers.IntegerField()
