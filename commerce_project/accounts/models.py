from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Personne(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    adresse = models.JSONField(default=list, blank=True, null=True)
    contact = models.CharField(max_length=100, default="", blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username