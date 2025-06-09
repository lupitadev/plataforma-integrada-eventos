from django.db import models
from django.contrib.auth.models import User
from home.models import Event

# Create your models here.


class VirtualEvent(Event):
    link = models.URLField(verbose_name="Enlace de acceso")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "Evento Virtual"
        verbose_name_plural = "Eventos Virtuales"
        ordering = ["-date"]

    def __str__(self):
        return self.title
