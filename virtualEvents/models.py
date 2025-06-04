from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime


class VirtualEvent(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    date = models.DateTimeField(verbose_name="Fecha y Hora")
    link = models.URLField(verbose_name="Enlace de acceso")
    image = models.ImageField(upload_to='virtual_events/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    fecha_texto = "2025-06-04 15:00:00"  # Fecha en formato de texto
    fecha_objeto = datetime.strptime(fecha_texto, "%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Evento Virtual"
        verbose_name_plural = "Eventos Virtuales"
        ordering = ['-date']

    def __str__(self):
        return self.title
