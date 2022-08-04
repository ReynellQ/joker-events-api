from cgitb import handler
from urllib import response
from django.http import JsonResponse,HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.views import View
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from activities.models import Activity, ActivityInscription
from activities.serializer import ActivitySerializer, ActivityIDSerializer
from participants.cancellations import CancellationRequests



from participants.models import Devolution, Participant, EventInscription
from users.models import Rol

import json

from events.serializer import EventIDSerializer, EventSerializer
from events.models import Events

from participants.serializer import CancellationRequestSerializer, InscriptionSerializer, ParticipantSerializer

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class ActivitiesView(View):
    def get(self, request):
        return JsonResponse(ActivitySerializer(Activity.objects.all(), many = True).data, safe = False)


    def post(self,request):
        if not request.user.is_authenticated or request.user.profile.rol != Rol.OP:
            return HttpResponseForbidden()
        requestData: dict = json.loads(request.body.decode('utf-8'))
        response = {}
        if requestData.get("id") == None:
            serializer : ActivitySerializer = ActivitySerializer(data = requestData)
            if serializer.is_valid():
                try:
                    serializer.save()
                    response = {"status" : True, "msg" : "Actividad creada"}
                except Exception as e:
                    response = {"status" : False, "msg" : "Ocurrió un error"}
            else:
                response = {"status" : False, "msg" : serializer.errors}
        else:
            try:
                a : Activity = Activity.objects.get(id = requestData.get("id"))
                serializer : ActivityIDSerializer = ActivityIDSerializer(a, data = requestData)
                if serializer.is_valid():
                    try:
                        serializer.save()
                        response ={"status" : True, "msg" : "Actividad modificada"}
                    except Exception as e:
                        print(repr(e))
                        response = {"status" : False, "msg" : "Ocurrió un error"}
                else:
                    response = {"status" : False, "msg" : serializer.errors}
            except Activity.DoesNotExist as dne:
                response = {"status" : False, "msg" : "No existe la actividad"}
            
        return JsonResponse(response)

            


@method_decorator(csrf_exempt, name='dispatch')
class EventActivitiesView(View):
    def get(self, request, event_id):
        if request.user.is_authenticated and request.user.profile.rol == Rol.PAR:
            return showMyActivities(request, event_id)
        response = []
        try:
            e : Events = Events.objects.get(id = event_id)
            act = Activity.objects.filter(idEvent = e)
            serializer = ActivityIDSerializer(act, many = True)
            response = serializer.data
        except Events.DoesNotExist as dne:
            response = []
        return JsonResponse(response, safe = False)

def showMyActivities(request, event_id):
    participant = request.user.profile.participant
    print(participant)
    
    try:
        e : Events = Events.objects.get(id = event_id)

        query = ActivityInscription.objects.filter(idParticipant = participant)
        query = list(map(lambda x : x.idActivity , query))
        query = [ q for q in query if q.idEvent == e]
        serializer = ActivityIDSerializer(query, many = True)
        response = serializer.data
        print(query)
    except Events.DoesNotExist as dne:
        response = []
    return JsonResponse(response, safe = False)
        
