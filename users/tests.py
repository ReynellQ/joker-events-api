from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
# Create your tests here.


class UserModelTest(TestCase):

    def test_user_with_correct_data(self):
        """
            The method checkData() for model Profile must return True if the data is correct.
        """
        dataUser = {
            "first_name": "Alfredo", "last_name": "Gonzalez", "username": "alfredo_gonzalez@gmail.com", "is_active": True,
            "password": "contraseña", "email": "alfredo_gonzalez@gmail.com"
        }
        dataProfile = {
            "rol": "admin", "address": "Calle 40#35-42", "telefono": "23412432", "ciudad": "Cali"
        }
        u: User = User(**dataUser)
        p: Profile = Profile(**dataProfile)
        u.profile = p
        self.assertIs(u.profile.checkData(), True)

        self.assertEquals(u.profile.getErrors(), [])

    def test_user_with_incorrect_role(self):
        """
            The method checkData() for model Profile must return False if the role is not "Administrador", "Gerente" or "Operador"
        """
        dataUser = {
            "first_name": "Alfredo", "last_name": "Gonzalez", "username": "alfredo_gonzalez@gmail.com", "is_active": True,
            "password": "contraseña", "email": "alfredo_gonzalez@gmail.com"
        }
        dataProfile = {
            "rol": "asdasd", "address": "Calle 40#35-42", "telefono": "23412432", "ciudad": "Cali"
        }
        u: User = User(**dataUser)
        p: Profile = Profile(**dataProfile)
        u.profile = p
        self.assertIs(u.profile.checkData(), False)
        self.assertEquals(u.profile.getErrors(), ["Incorrect role"])

    def test_user_with_wrong_password(self):
        """
            The method checkData() for model Profile must return False if the password doesn't have a length of 8 or more 
            characters
        """
        dataUser = {
            "first_name": "Alfredo", "last_name": "Gonzalez", "username": "alfredo_gonzalez@gmail.com", "is_active": True,
            "password": "aaa", "email": "alfredo_gonzalez@gmail.com"
        }
        dataProfile = {
            "rol": "admin", "address": "Calle 40#35-42", "telefono": "23412432", "ciudad": "Cali"
        }
        u: User = User(**dataUser)
        p: Profile = Profile(**dataProfile)
        u.profile = p
        self.assertIs(u.profile.checkData(), False)

        self.assertEquals(u.profile.getErrors(), ["Incorrect password"])

    def test_user_with_wrong_email(self):
        """
            The method checkData() for model Profile must return False if the password doesn't have a correct email
        """
        dataUser = {
            "first_name": "Alfredo", "last_name": "Gonzalez", "username": "peppapig@", "is_active": True,
            "password": "contraseña", "email": "peppapig@"
        }
        dataProfile = {
            "rol": "admin", "address": "Calle 40#35-42", "telefono": "23412432", "ciudad": "Cali"
        }
        u: User = User(**dataUser)
        p: Profile = Profile(**dataProfile)
        u.profile = p
        self.assertIs(u.profile.checkData(), False)
        self.assertEquals(u.profile.getErrors(), ["Incorrect email"])

    def test_user_with_wrong_data(self):
        """
            The method checkData() for model Profile must return False if all the previous fields are wrong simulteanously,
            and show all the errors
        """
        dataUser = {
            "first_name": "Alfredo", "last_name": "Gonzalez", "username": "peppapig@", "is_active": True,
            "password": "lala", "email": "peppapig@"
        }
        dataProfile = {
            "rol": "asdasdad", "address": "Calle 40#35-42", "telefono": "23412432", "ciudad": "Cali"
        }
        u: User = User(**dataUser)
        p: Profile = Profile(**dataProfile)
        u.profile = p
        self.assertIs(u.profile.checkData(), False)

        self.assertEquals(u.profile.getErrors(),
                          ["Rol inexistente", "Password no permitida", "Email invalido"])
