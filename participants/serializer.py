from datetime import datetime
from email.policy import default
from django.utils import timezone
from activities.models import Activity, ActivityInscription
from rest_framework import serializers

from django.db import transaction
from django.utils.translation import gettext as _
from noticias.models import News
from django.contrib.auth.models import User
from participants.models import Devolution, EventInscription, Participant
from users.models import Profile, Rol
from events.models import Events
from users.serializer import UserSerializer


class ParticipantSerializer(UserSerializer):
    """
        A serializer to display and create a Participant
    """
    cedula =  serializers.CharField()
    birthday = serializers.DateField()

    @staticmethod
    def make_map(x : Participant):
        p : Profile = x.profile
        return {
                "cedula": x.cedula,
                "nombre" : p.user.first_name,
                "apellido" : p.user.last_name,
                "email" : p.user.username,
                "ciudad": p.ciudad,
                "telefono" : p.telefono,
                "address" : p.address,
                "birthday" : x.birthdate
            }
    @staticmethod
    def getSerializedModel(model):
        return ParticipantSerializer(ParticipantSerializer.make_map(model)).data

    @staticmethod
    def getSerializedModels(models):
        return [ParticipantSerializer.getSerializedModel(model) for model in models]


    
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
    
    def to_representation(self, instance : User):
        print(instance)
        ret = super().to_representation(instance)
        p : Participant = instance.profile.participant
        ret['cedula'] = p.cedula
        ret['birthday'] = p.birthdate
        return ret

class PaymentSerializer(serializers.Serializer):
    nameOnCard = serializers.CharField()
    cardNumber = serializers.CharField(min_length = 16, max_length = 16)
    expiryDate = serializers.DateField()
    cvv = serializers.CharField(min_length = 3, max_length = 4)

    def validate_expiryDate(self, value):
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
        try:
            instance = Participant.objects.get(cedula = value["cedula"])
            p.instance = instance
        except Exception as e:
            p = ParticipantSerializer(data = value)
            p.is_valid()
            p.save()
            print(p.instance)
            
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
            idParticipant = participant, status = EventInscription.Status.INSCRITO, registerDate = timezone.now()
            )
        print(self.validated_data["actividades"])
        for id_activity in self.validated_data["actividades"]:
            a : Activity = Activity.objects.get(id = id_activity)
            act_inscription : ActivityInscription = ActivityInscription.objects.create(
                idActivity = a, idParticipant = participant, registerDate = timezone.now()
            )
        print(inscription)
        
        
class CancellationRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(required = False)
    cedula = serializers.CharField()
    evento = serializers.IntegerField()
    nombre = serializers.CharField(required = False)
    apellido = serializers.CharField(required = False)
    valor = serializers.DecimalField(required = False,
        default=0.0, max_digits=14, decimal_places=2)
    diasRestantes = serializers.IntegerField(required = False)
    motivo = serializers.CharField()
    solicitudDate = serializers.DateTimeField(required = False, default= timezone.now())

    def to_representation(self, instance : Devolution):
        ei : EventInscription = instance.inscription
        e : Events = ei.idEvent
        p : Participant = ei.idParticipant
        pro : Profile = p.profile
        u : User = pro.user
        ret = {
                'id' : instance.id,
                'cedula' : p.cedula,
                'evento' : e.id,
                'nombre' : u.first_name,
                'apellido' : u.last_name,
                'valor' : e.precioBoleta,
                'diasRestantes' : (e.fechaInicio - instance.solicitudDate).days,
                'motivo' : instance.motivo,
                'solicitudDate' : instance.solicitudDate
            }
        return ret

    def create(self, validated_data):
        with transaction.atomic():
            e : Events = Events.objects.get(id = validated_data["evento"])
            p : Participant = Participant.objects.get(cedula = validated_data["cedula"])
            ei : EventInscription = EventInscription.objects.get(idEvent = e, status = EventInscription.Status.INSCRITO, idParticipant = p)
            ei.status = EventInscription.Status.DEVOLUCION
            ei.save()
            d: Devolution = Devolution(inscription = ei, motivo = validated_data["motivo"], solicitudDate = validated_data["solicitudDate"])
            d.save()
            return d
    def delete(self, instruction):
        d : Devolution = self.instance
        if instruction:
            with transaction.atomic():
                
                inscription : EventInscription = d.inscription
                event : Events = inscription.idEvent
                event.disponible+=1
                event.save()
                inscription.status = EventInscription.Status.CANCELADO
                inscription.save()
                d.delete()
                #Enviar correo
        else:
            d.delete()
            #Enviar corre