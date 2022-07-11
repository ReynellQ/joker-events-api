from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


import json

from events.serializer import EventIDSerializer
from events.models import Events

from participants.serializer import InscriptionSerializer, ParticipantSerializer

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class ParticipantView(View):
    def post(self,request):
        try:
            requestData: dict = json.loads(request.body.decode('utf-8'))
            serializer = InscriptionSerializer(data = requestData)
            if serializer.is_valid():
                with transaction.atomic():
                    serializer.process()
                    raise Exception("ONLY FOR ROLLBACK PURPOSES")
            else:
                raise Exception(serializer.errors)
            # participant = ParticipantSerializer(data = requestData["participante"])
            
            # with transaction.atomic():
            #     if not participant.is_valid():
            #         raise Exception(participant.errors)
            #     if participant.getParticipant() != None:
            #         p = participant.getParticipant()
            #     else:
            #         p = participant.save()
                    
            #     event : Events= Events.objects.get(id=requestData["evento"])
            #     event.disponible-=1
            #     event.save()
            #     if event.description < 0:
            #         raise Exception("El evento no tiene aforo")
                
            return JsonResponse({"status" : True})
        except Exception as e:
            print(repr(e))
            print(e.args)
            return JsonResponse({"status" : False})
        