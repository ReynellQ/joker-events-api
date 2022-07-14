from django.db import models
from django.contrib.auth.models import User
from users.models import Rol

from django.utils import timezone
from datetime import datetime
import pytz

utc = pytz.UTC

# Create your models here.


class News(models.Model):
    title = models.TextField(blank=False)
    description = models.TextField()
    image = models.CharField(max_length=200, blank=True)
    publishedAt = models.DateTimeField("date published")
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    visible = models.BooleanField(blank=False)

    class Meta:
        ordering = ('-publishedAt',)
    def __str__(self):
        return self.title + " " + str(self.publishedAt) + " " + str(self.createdBy)
