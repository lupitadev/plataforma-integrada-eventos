from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


# Modelo de Usuario personalizado
class User(AbstractUser):
    TIPOS = [
        ('ASISTENTE', 'Asistente'),
        ('ORGANIZADOR', 'Organizador'),
    ]
    from django.contrib.auth.models import Group, Permission

    groups = models.ManyToManyField(Group, related_name="home_usuario_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="home_usuario_permissions")
    tipo_usuario = models.CharField(max_length=11, choices=TIPOS)
    telefono = models.CharField(max_length=15, blank=True)


# Modelo para Eventos (común para ambos tipos)
class Event(models.Model):
    TIPOS = [
        ('VIRTUAL', 'Virtual'),
        ('PRESENCIAL', 'Presencial'),
    ]
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPOS)
    fecha = models.DateTimeField()
    imagen = models.ImageField(upload_to='eventos/')
    destacado = models.BooleanField(default=False)

    # Campos específicos para virtuales
    enlace_virtual = models.URLField(blank=True)

    # Campos específicos para presenciales
    direccion = models.TextField(blank=True)
    ciudad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.titulo
