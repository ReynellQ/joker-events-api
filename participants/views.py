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
            else:
                raise Exception(serializer.errors)
            return JsonResponse({"status" : True})
        except Exception as e:
            return JsonResponse({"status" : False, "msg" : e.args[0]})
        