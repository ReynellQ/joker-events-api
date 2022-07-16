from django.utils import timezone
from django.http import HttpRequest, JsonResponse
from django.db.utils import IntegrityError
from django.views import View
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.db.models.functions import Lower
from participants.serializer import ParticipantSerializer

from users.serializer import UserSerializer
from .models import Profile
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
import json
from django.views.decorators.csrf import csrf_exempt
from users.models import Rol
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class Users(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.profile.rol == Rol.ADMIN

    def get(self, request):
        try:
            list = User.objects.select_related(
                'profile').order_by(Lower('first_name'))

            users = []
            for user in list:
                u: User = user
                if u.profile.rol != Rol.PAR:
                    users.append(UserSerializer(u).data)
            return JsonResponse({"data": users}, safe = False)
        except Exception as e:
            print(repr(e))
            return JsonResponse({"msg": 'an error occured'})

    def post(self, request):
        response = {}
        try:
            content = json.loads(request.body.decode('utf-8'))
            action = content["action"]
            dataUser = {
                "username": content["email"], "first_name": content["nombre"], "last_name": content["apellido"],
                "is_active": bool(content["enabled"]), "email": content["email"], "password": content["password"],
            }
            dataProfile = {
                "rol": content["rol"], "address": content["address"], "telefono": content["telefono"], "ciudad": content["ciudad"]
            }
            if action == 'create':
                response = createUser(dataUser, dataProfile)
            else:
                response = modifyUser(dataUser, dataProfile)
        except IntegrityError as ie:
            print(repr(ie))
            response["status"] = False
            response["msg"] = "Ya existe un usuario con dicho correo"
        except Exception as e:
            response["status"] = False
            print(repr(e))
            response["msg"] = "Formato Incorrecto"
        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class Auth(View):
    def get(self, request):
        res = {}
        res["status"] = request.user.is_authenticated
        if res["status"]:
            res["msg"] = ParticipantSerializer(request.user).data if request.user.profile.rol == Rol.PAR else UserSerializer(request.user).data
        return JsonResponse(res)

    def post(self, request):
        try:
            res = {}
            data = json.loads(request.body.decode('utf-8'))
            username = data["email"]
            password = data["password"]
            user = auth.authenticate(username=username, password=password)
            res["status"] = user is not None
            print(user)
            if res["status"]:
                res["msg"] = ParticipantSerializer(user).data if user.profile.rol == Rol.PAR else UserSerializer(user).data
                auth.login(request, user)
            else:
                res["msg"] = "No pudo logearse"
            return JsonResponse(res)
        except Exception as e:
            print(repr(e))
            return JsonResponse({"err": "User not authenticated"})

    def delete(self, request):
        try:
            auth.logout(request)
            return JsonResponse({"res": True})
        except Exception as e:
            print(repr(e))
            return JsonResponse({"res": False, "message": "Ocurrio un error en el logout"})


def createUser(dataUser, dataProfile):
    dataUser["date_joined"] = timezone.now()
    print(dataProfile)
    up = Profile(**dataProfile)
    u = User(**dataUser)
    up.user = u
    u.profile = up
    if not u.profile.checkData():
        return {"status": False, "msg": u.profile.getErrors()}
    u = User.objects.create_user(**dataUser)
    for attr, value in dataProfile.items():
        setattr(u.profile, attr, value)
    u.save()
    return {"status": True, "msg": "Usuario creado"}


def modifyUser(dataUser, dataProfile):
    try:
        newPass = dataUser.pop("password", None)
        u: User = User.objects.get(username=dataUser["username"])
        User.objects.filter(username=dataUser["username"])
        if newPass != "" or newPass is None:
            u.password = newPass
        for attr, value in dataUser.items():
            setattr(u, attr, value)
        for attr, value in dataProfile.items():
            setattr(u.profile, attr, value)
        if u.profile.checkData():
            if newPass != "" or newPass is None:
                u.set_password(newPass)
            u.save()
            return {"status": True, "msg": "Usuario modificado correctamente"}
        else:
            return {"status": False, "msg": u.profile.getErrors()}

    except Exception as e:
        print(repr(e))
        return {"status": False, "msg": "No existe el usuario"}
