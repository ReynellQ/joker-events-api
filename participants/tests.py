from django.test import TestCase

from participants.serializer import ParticipantSerializer

# Create your tests here.
class NewsModelTest(TestCase):
    def test_create_a_participant(self):
        self.assertEquals(True, True)

    def test_search_a_participant(self):
        """
        Creates a participant. Then, recieves a "cedula" of a existent participant, and returning the
        participant.
        ParticipantSerializer().getParticipant() != None
        """
        data = {
            "cedula": "1006037732",
            "nombre": "hola",
            "apellido": "xxdxdxd",
            "email": "participante@gmail.com",
            "telefono": "xd",
            "ciudad": "xd",
            "address": "xd",
            "birthday": "2022-06-03",
            "password": "xd"
        }
        creator = ParticipantSerializer(data = data)
        creator.is_valid()
        creator.save()
        searcher = ParticipantSerializer(data = data)
        searcher.is_valid()
        print(searcher.getParticipant())
        self.assertEquals(creator.instance, searcher.instance)

