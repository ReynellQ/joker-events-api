from django.db import models
from django.contrib.auth.models import User
from users.models import Rol

from django.utils import timezone
from datetime import datetime
import pytz

utc = pytz.UTC

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=200)
    image = models.CharField(max_length=200, blank=True)
    publishedAt = models.DateTimeField("date published")
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    visible = models.BooleanField(blank=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.checkAttributes():
            raise ValueError("Los campos no son correctos")
        super().save(*args, **kwargs)

    def checkAttributes(self):
        print(datetime.strptime(self.publishedAt, "%Y-%m-%dT%H:%M:%SZ"))
        date = utc.localize(datetime.strptime(
            self.publishedAt, "%Y-%m-%dT%H:%M:%SZ"))
        if self.title == "":
            return False
        if self.description == "":
            return False
        if date > timezone.now():
            return False
        if not self.createdBy.profile.rol == Rol.OP:
            return False
        return True
