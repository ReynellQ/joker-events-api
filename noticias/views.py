from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from noticias.handler import BaseHandler, CheckCorrectData, CheckUserExistance, CheckNewExistance
import json

from noticias.models import News
from noticias.serializer import NewsSerializer, NewsIDSerializer
from users.models import Rol


# Create your views here.

def Public_News(request):
    response = NewsSerializer(News.objects.filter(visible=True), many=True)
    return JsonResponse(response.data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class NewsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.profile.rol == Rol.OP

    def get(self, request):
        response = NewsIDSerializer(News.objects.all(), many=True)
        return JsonResponse(response.data, safe=False)

    def post(self, request):
        data: dict = json.loads(request.body.decode('utf-8'))
        response = {}
        if "id" in data.keys():
            bh = BaseHandler(data)
            h1 = CheckNewExistance(data)
            h2 = CheckUserExistance(data)
            h3 = CheckCorrectData(data)
            h2.setNext(h3)
            h1.setNext(h2)
            bh.setNext(h1)
            response = bh.handle()

            return JsonResponse(response)
        else:
            bh = BaseHandler(data)
            h1 = CheckUserExistance(data)
            h2 = CheckCorrectData(data)
            h1.setNext(h2)
            bh.setNext(h1)
            response = bh.handle()
            return JsonResponse(response)

    def delete(self, request):
        data: dict = json.loads(request.body.decode('utf-8'))
        ch = CheckNewExistance(data)
        response = ch.handle()
        print(response.get("status"))
        if response.get("status"):
            News.objects.filter(id=data["id"]).delete()
        return JsonResponse(response)
