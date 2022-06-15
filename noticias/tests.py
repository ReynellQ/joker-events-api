from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from users.models import Rol
from noticias.serializer import NewsSerializer

# Create your tests here.


class NewsModelTest(TestCase):
    def setUp(self) -> None:
        dataUser = {
            "username": 'operador@yopmail.com', "first_name": 'Reynell', "last_name": 'Quevedo',
            "is_active": True, "email": 'operador@yopmail.com', "password": '12345678',
        }
        u: User = User.objects.create_user(**dataUser)
        u.profile.rol = Rol.OP
        u.save()

    def test_with_correct_data(self):
        data = {
            "title": "asd",
            "description": " asdasda",
            "publishedAt": timezone.now(),
            "createdBy": 'operador@yopmail.com',
            'visible': True
        }
        n = NewsSerializer(data=data)
        res = n.is_valid(raise_exception=True)
        print(n.save())
        self.assertEquals(res, True)
