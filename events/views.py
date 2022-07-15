from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from events.models import Events, MediaEvents

from events.serializer import EventSerializer, EventIDSerializer
from users.models import Rol

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class EventView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.profile.rol == Rol.OP

    def get(self, request):
        query = Events.objects.all().order_by('fechaInicio')
        response = EventIDSerializer(query, many = True).data
        return JsonResponse(response, safe=False)


    def post(self, request):
        requestData: dict = json.loads(request.body.decode('utf-8'))
        requestData["createdBy"] = request.user.email
        response = {}

        if "id" in requestData.keys():
            serializer = EventIDSerializer(data=requestData)
        else:
            serializer = EventSerializer(data=requestData)
        response["status"] = serializer.is_valid()
        if response["status"]:
            serializer.save()
            response["msg"] = serializer.text
        else:
            response["msg"] = serializer.errors
        
        return JsonResponse(response)
