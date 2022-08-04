from cgitb import handler
from urllib import response
from django.http import JsonResponse,HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.views import View
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from participants.cancellations import CancellationRequests



from participants.models import Devolution, Participant, EventInscription
from users.models import Rol

import json

from events.serializer import EventIDSerializer, EventSerializer
from events.models import Events

from participants.serializer import CancellationRequestSerializer, InscriptionSerializer, ParticipantSerializer

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class ParticipantView(View):
    def get(self, request):
        if not request.user.is_authenticated or request.user.profile.rol != Rol.PAR:
            return HttpResponseForbidden()
        p : Participant = Participant.objects.get(profile = request.user.profile)
        listOfEvents = [q.idEvent for q in EventInscription.objects.filter(idParticipant = p, status = EventInscription.Status.INSCRITO)]

        listOfEvents = EventIDSerializer(listOfEvents, many = True).data
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
            listOfParticipants = [q.idParticipant.profile.user for q in EventInscription.objects.filter(idEvent = e, status = EventInscription.Status.INSCRITO)]
            print(listOfParticipants)
            response = ParticipantSerializer(listOfParticipants, many = True).data
        except Exception as e:
            print(repr(e))
        return JsonResponse(response, safe = False)
        

    def delete(self, request, event_id):
        if not request.user.is_authenticated or request.user.profile.rol != Rol.PAR:
            return HttpResponseForbidden()
        response = {}
        try:
            requestData: dict = json.loads(request.body.decode('utf-8'))
            e : Events = Events.objects.get(id = event_id)
            p : Participant = Participant.objects.get(profile = request.user.profile)
            ei : EventInscription = EventInscription.objects.get(idEvent = e, status = EventInscription.Status.INSCRITO, idParticipant = p)
            requestData["cedula"] = p.cedula
            requestData["evento"] = event_id
            serializer = CancellationRequestSerializer(data = requestData)
            
            if serializer.is_valid():
                serializer.save()
                response = {"status" : True, "msg" : "Solicitud de devolución enviada correctamente"}
            else:
                response = {"status" : False, "msg" : serializer.errors}
        except EventInscription.DoesNotExist as dne:
            response = {"status" : False, "msg" : "No existe dicha solicitud."}
        except Exception as e:
            response = {"status" : False, "msg" : "No se pudo procesar la solicitud."}

        
        return JsonResponse(response)

        
@method_decorator(csrf_exempt, name='dispatch')
class DevolutionView(View):
    def get(self, request):
        if not request.user.is_authenticated or request.user.profile.rol != Rol.OP:
            return HttpResponseForbidden()
        response = {}
        serializer = CancellationRequestSerializer(Devolution.objects.all(), many = True)
        return JsonResponse(serializer.data, safe = False)
        

    def post(self, request):
        if not request.user.is_authenticated or request.user.profile.rol != Rol.OP:
            return HttpResponseForbidden()
        try:
            requestData: dict = json.loads(request.body.decode('utf-8'))
            serializer = CancellationRequestSerializer(Devolution.objects.get(id = requestData["id"]))
            serializer.delete(requestData["answer"])
            response = {"status" : True, "msg" : "Solicitud procesada correctamente"}
        except Devolution.DoesNotExist as dne:
            response = {"status" : False, "msg" : "No existe dicha solicitud."}
        except Exception as e:
            print(repr(e))
            response = {"status" : False, "msg" : "No se pudo procesar la solicitud."}

        
        return JsonResponse(response)