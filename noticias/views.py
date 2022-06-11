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
from users.models import Rol


# Create your views here.

def Public_News(request):
    def parseData(x):
        id = x["pk"]
        x = x["fields"]
        u: User = User.objects.get(id=x["createdBy"])
        x["createdBy"] = u.email
        return x
    response = News.objects.filter(visible=True)
    response = serialize('json', response)
    response = json.loads(response)
    print(response)
    response = list(map(lambda x: parseData(x), response))
    return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class NewsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.profile.rol == Rol.OP

    def get(self, request):
        def parseData(x):
            id = x["pk"]
            x = x["fields"]
            u: User = User.objects.get(id=x["createdBy"])
            x["createdBy"] = u.email
            x["id"] = id
            return x
        response = News.objects.all()
        response = serialize('json', response)
        response = json.loads(response)
        print(response)
        response = list(map(lambda x: parseData(x), response))
        return JsonResponse(response, safe=False)

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
