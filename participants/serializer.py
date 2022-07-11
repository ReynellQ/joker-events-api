
from django.utils import timezone
from rest_framework import serializers

from django.utils.translation import gettext as _
from noticias.models import News
from django.contrib.auth.models import User
from participants.models import EventInscription, Participant
from users.models import Profile, Rol
from events.models import Events

class ParticipantSerializer(serializers.Serializer):
    """
        A serializer to display and create a Participant
    """
    cedula =  serializers.CharField()
    nombre = serializers.CharField()
    apellido = serializers.CharField()
    email = serializers.EmailField()
    ciudad = serializers.CharField()
    telefono = serializers.CharField()
    address = serializers.CharField()
    birthday = serializers.DateField()
    password = serializers.CharField()

    def getParticipant(self):
        p = None
        try:
            p = Participant.objects.get(cedula = self.data["cedula"])
            self.instance = p
        except Exception as e:
            print(repr(e))
        return p

    
    def create(self, data):
        dataUser ={
            "username":data["email"], "first_name":data["nombre"], "last_name" : data["apellido"],
            "is_active":True, "email" :data["email"], "password" : data["password"]
        } 
        u = User.objects.create_user(**dataUser)
        dataProfile = {
            "rol": "participante", "address":data["address"], "ciudad":data["ciudad"],
            "telefono": data["telefono"]
        }
        for attr, value in dataProfile.items():
            setattr(u.profile, attr, value)
        u.save()
        p = Participant(profile = u.profile, cedula = data["cedula"], birthdate = data["birthday"])
        p.save()
        
        return p

class PaymentSerializer(serializers.Serializer):
    nameOnCard = serializers.CharField()
    cardNumber = serializers.CharField(min_length = 16, max_length = 16)
    expiryDate = serializers.DateField()
    cvv = serializers.CharField(min_length = 3, max_length = 4)

    def validate_expiryDate(self, value):
        print(type(value))
        if value < timezone.now().date():
            raise serializers.ValidationError("The card is expired")
        return value


class InscriptionSerializer(serializers.Serializer):
    participante = ParticipantSerializer()
    evento = serializers.IntegerField()
    payment = PaymentSerializer()
    actividades = serializers.ListField(
        child=serializers.IntegerField()
    )

    def validate_participante(self, value):
        p = ParticipantSerializer(data = value)
        if not p.is_valid():
            raise serializers.ValidationError(p.errors)
        if p.getParticipant() == None:
            p = ParticipantSerializer(data = value)
            p.is_valid()
            p.save()
        return p
    
    def validate_evento(self, value):
        try:
            Events.objects.get(id = value)
        except:
            raise serializers.ValidationError("The event doesn't exists.")
        return int(value)

    def validate_payment(self, value):
        from random import randint
        p = PaymentSerializer(data = value)
        if p.is_valid():
            r = randint(0, 10)
            if r <= 8:
                return p
            else:
                raise Exception("Ocurrio un error validando sus datos de pago")
        else:
            return serializers.ValidationError(p.errors)

    def process(self):
        event : Events= Events.objects.get(id=self.validated_data["evento"])
        event.disponible-=1
        event.save()
        if event.disponible < 0:
            raise Exception("Full event")
        participant = self.validated_data["participante"].instance
        inscription = EventInscription.objects.filter(idEvent = event, idParticipant = participant)
        if inscription.count() != 0:
            raise Exception("Already registered in this event")
        inscription : EventInscription = EventInscription.objects.create(idEvent = event,
            idParticipant = participant, status = EventInscription.Status.PRE_INSCRITO, registerDate = timezone.now()
            )
        print(inscription)
        


