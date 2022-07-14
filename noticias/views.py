from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
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
        response = NewsIDSerializer(News.objects.all().order_by('-publishedAt'), many=True)
        return JsonResponse(response.data, safe=False)

    def post(self, request):
        requestData: dict = json.loads(request.body.decode('utf-8'))
        response = {}
        if "id" in requestData.keys():
            serializer = NewsIDSerializer(data=requestData)
        else:
            serializer = NewsSerializer(data=requestData)
        response["status"] = serializer.is_valid()
        if response["status"]:
            serializer.save()
            response["msg"] = serializer.text
        else:
            response["msg"] = serializer.errors
        return JsonResponse(response)

    def delete(self, request):
        response = {}
        requestData: dict = json.loads(request.body.decode('utf-8'))
        try:
            news = News.objects.get(id=requestData["id"])
            news.delete()
            response = {"status": True}
        except News.DoesNotExist as ndne:
            response = {"status": False}

        return JsonResponse(response)
