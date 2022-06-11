from noticias.models import News
from django.contrib.auth.models import User


class HandlerNewsValidation():
    def setNext(self, handler):
        pass

    def handle(self):
        pass


class BaseHandler(HandlerNewsValidation):
    news = News()
    correctResponse = {
        "status": True,
        "msg": "Correcto"
    }

    def __init__(self, data):
        self.data = data
        self.next = None

    def setNext(self, handler: HandlerNewsValidation):
        self.next = handler

    def handle(self):
        if self.next != None:
            return self.next.handle()
        BaseHandler.news = None
        return BaseHandler.correctResponse


class CheckUserExistance(BaseHandler):
    def __init__(self, data):
        super().__init__(data)

    def handle(self):
        try:
            BaseHandler.news.createdBy = User.objects.get(
                username=self.data.pop("createdBy"))
            return super().handle()
        except User.DoesNotExist as udne:
            return {
                "status": False,
                "msg": "No existe el usuario"
            }


class CheckNewExistance(BaseHandler):
    def __init__(self, data):
        super().__init__(data)

    def handle(self):
        try:
            BaseHandler.news = News.objects.get(id=self.data["id"])
            return super().handle()
        except News.DoesNotExist as dne:
            return {
                "status": False,
                "msg": "No existe la noticia"
            }


class CheckCorrectData(BaseHandler):
    def __init__(self, data):
        super().__init__(data)

    def handle(self):
        try:
            for attr, value in self.data.items():
                setattr(BaseHandler.news, attr, value)
            BaseHandler.news.save()
            return super().handle()
        except ValueError as ve:
            return {
                "status": False,
                "msg": "Datos incorrectos"
            }
