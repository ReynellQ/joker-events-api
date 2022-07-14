from django.http import JsonResponse,HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.views import View
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



from participants.models import Participant, EventInscription
from users.models import Rol

import json

from events.serializer import EventIDSerializer, EventSerializer
from events.models import Events

from participants.serializer import InscriptionSerializer, ParticipantSerializer

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class ParticipantView(View):
    def get(self, request):
        if not request.user.is_authenticated or request.user.profile.rol != Rol.PAR:
            return HttpResponseForbidden()
        p : Participant = Participant.objects.get(profile = request.user.profile)
        listOfEvents = [q.idEvent for q in EventInscription.objects.filter(idParticipant = p)]

        listOfEvents = EventSerializer.getSerializedModels(listOfEvents)
        return JsonResponse(listOfEvents, safe = False)


    def post(self,request):
        try:
            requestData: dict = json.loads(request.body.decode('utf-8'))
            serializer = InscriptionSerializer(data = requestData)
            if serializer.is_valid():
                with transaction.atomic():
                    serializer.process()
            else:
                raise Exception(serializer.errors)
            return JsonResponse({"status" : True})
        except Exception as e:
            return JsonResponse({"status" : False, "msg" : e.args[0]})
            
@method_decorator(csrf_exempt, name='dispatch')
class EventInscriptionView(View):
    def get(self, request, event_id):
        if not request.user.is_authenticated or request.user.profile.rol != Rol.OP:
            return HttpResponseForbidden()
        response = []
        try:
            e : Events = Events.objects.get(id = event_id)
            listOfParticipants = [q.idParticipant for q in EventInscription.objects.filter(idEvent = e, status = EventInscription.Status.INSCRITO)]
            response = ParticipantSerializer.getSerializedModels(listOfParticipants)
        except Exception as e:
            pass
        return JsonResponse(response, safe = False)
        

    def delete(self, request):
        pass

        