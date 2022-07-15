from django.db import transaction

from events.models import Events
from participants.models import EventInscription
from participants.serializer import CancellationRequestSerializer


class CancellationRequests(object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(CancellationRequests, self).__new__(self)
            self.requests = {}
        return self.instance
    
    def addRequest(self, request : CancellationRequestSerializer):
        with transaction.atomic():
            inscription : EventInscription = request.instance
            inscription.status = EventInscription.Status.DEVOLUCION
            inscription.save()
            self.requests[inscription.id] = request
        

    def listRequests(self):
        return list(self.requests.values())

    def accept(self, id):
        with transaction.atomic():
            request : CancellationRequestSerializer = self.requests[id]
            inscription : EventInscription = request.instance
            event : Events = inscription.idEvent
            event.disponible+=1
            event.save()
            inscription.status = EventInscription.Status.CANCELADO
            inscription.save()
            return self.requests.pop(id)
        

    def reject(self, id):
        pass
    