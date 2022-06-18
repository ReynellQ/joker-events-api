import datetime
from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from users.models import Rol
from noticias.serializer import NewsSerializer
from django.utils.translation import gettext as _

# Create your tests here.


class NewsModelTest(TestCase):
    def setUp(self) -> None:
        dataUser = {
            "username": 'operador@yopmail.com', "first_name": 'Reynell', "last_name": 'Quevedo',
            "is_active": True, "email": 'operador@yopmail.com', "password": '12345678',
        }
        u1: User = User.objects.create_user(**dataUser)
        u1.profile.rol = Rol.OP
        u1.save()

        dataUser = {
            "username": 'admin@yopmail.com', "first_name": 'Reynell', "last_name": 'Quevedo',
            "is_active": True, "email": 'admin@yopmail.com', "password": '12345678',
        }
        u2: User = User.objects.create_user(**dataUser)
        u2.profile.rol = Rol.ADMIN
        u2.save()

    def test_with_correct_data(self):
        """
        Create a news with correct data.
        It has no errors.
        """
        data = {
            "title": "asd",
            "description": " asdasda",
            "publishedAt": timezone.now(),
            "createdBy": 'operador@yopmail.com',
            'visible': True
        }
        n = NewsSerializer(data=data)
        res = n.is_valid(raise_exception=True)
        errors = n.errors
        self.assertEquals(res, True)
        self.assertEquals(0, len(errors))

    def test_with_incorrect_role(self):
        """
        Create a news with correct data, but the creator hasn't the correct role.
        This is the unique error displayed.
        """
        data = {
            "title": "asd",
            "description": " asdasda",
            "publishedAt": timezone.now(),
            "createdBy": 'admin@yopmail.com',
            'visible': True
        }
        n = NewsSerializer(data=data)
        res = n.is_valid()
        errors = n.errors
        self.assertEquals(res, False)
        self.assertEquals("The creator isn't a operator.",
                          errors.pop('createdBy')[0])
        self.assertEquals(0, len(errors))

    def test_without_user(self):
        """
        Create a news with correct data, but the creator doesn't exists.
        This is the unique error displayed.
        """
        data = {
            "title": "asd",
            "description": " asdasda",
            "publishedAt": timezone.now(),
            "createdBy": 'asdasdasda',
            'visible': True
        }
        n = NewsSerializer(data=data)
        res = n.is_valid()
        errors = n.errors
        self.assertEquals(res, False)
        self.assertEquals("User doesn't exists.",
                          errors.pop('createdBy')[0])
        self.assertEquals(0, len(errors))

    def test_without_a_other_field(self):
        """
        Create a news without one field. This field is variable and is one of the
        required fields.
        This is the unique error displayed.
        """
        field = 'description'
        data = {
            "title": "asd",
            "publishedAt": timezone.now(),
            "createdBy": 'operador@yopmail.com',
            'visible': True
        }
        n = NewsSerializer(data=data)
        res = n.is_valid()
        errors = n.errors
        self.assertEquals(res, False)
        self.assertEquals('This field is required.',
                          errors.pop(field)[0])

        self.assertEquals(0, len(errors))

    def test_with_posterior_date(self):
        """
            Create a news with a publication date 1 day after this instant, which is incorrect.
            This is the unique error displayed.
        """
        data = {
            "title": "asd",
            "description": " asdasda",
            "publishedAt": timezone.now() + datetime.timedelta(days=1),
            "createdBy": 'operador@yopmail.com',
            'visible': True
        }
        n = NewsSerializer(data=data)
        res = n.is_valid()
        errors = n.errors
        self.assertEquals(res, False)
        self.assertEquals('Date is incorrect.',
                          errors.pop('publishedAt')[0])

        self.assertEquals(0, len(errors))

    def test_with_incorrect_date(self):
        """
            Create a news with a publication date that is not a datetime string.
            This is the unique error displayed.
        """
        data = {
            "title": "asd",
            "description": " asdasda",
            "publishedAt": 'sdasdasd',
            "createdBy": 'operador@yopmail.com',
            'visible': True
        }
        n = NewsSerializer(data=data)
        res = n.is_valid()
        errors = n.errors
        self.assertEquals(res, False)
        self.assertEquals(
            True, 'Datetime has wrong format' in errors.pop('publishedAt')[0])

        self.assertEquals(0, len(errors))

    def test_with_incorrect_data(self):
        """
            Create a news with multiple errors:
                - The user exists but isn't a operator
                - Has no description
                - Has incorrect date
            It must display all the errors
        """
        data = {
            "title": "asd",
            "publishedAt": 'sdasdasd',
            "createdBy": 'admin@yopmail.com',
            'visible': True
        }
        n = NewsSerializer(data=data)
        res = n.is_valid()
        errors = n.errors
        self.assertEquals(res, False)
        self.assertEquals(
            True, 'Datetime has wrong format' in errors.pop('publishedAt')[0])
        self.assertEquals('This field is required.',
                          errors.pop('description')[0])
        self.assertEquals("The creator isn't a operator.",
                          errors.pop('createdBy')[0])

        self.assertEquals(0, len(errors))
