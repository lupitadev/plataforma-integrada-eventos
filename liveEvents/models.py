from django.db import models
from home.models import User
from django.utils.timezone import now


# Create your models here.


class LiveEvent(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(default="No description available", verbose_name="Descripción")
    date = models.DateTimeField(default=now, verbose_name="Fecha y hora")
    image = models.ImageField(upload_to='virtual_events/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)
