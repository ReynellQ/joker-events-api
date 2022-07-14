from django.db import transaction

from events.models import Events
from participants.models import EventInscription


class CancellationRequests(object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(CancellationRequests, self).__new__(self)
            self.requests = {}
        return self.instance
    
    def addRequest(self, request : EventInscription):
        self.requests[request.id] = request
        pass

    def listRequests(self):
        pass

    def accept(self, id):
        with transaction.atomic():
            request : EventInscription = self.requests[id]
            event : Events = request.idEvent
            event.disponible+=1
            event.save()
            request.status = EventInscription.Status.CANCELADO


    def reject(self, id):
        pass
    