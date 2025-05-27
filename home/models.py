from django.db import models
from django.urls import reverse

# Create your models here.
from django.contrib.auth.models import AbstractUser


# Modelo de Usuario personalizado
class User(AbstractUser):
    TIPOS = [
        ("ASISTENTE", "Asistente"),
        ("ORGANIZADOR", "Organizador"),
    ]
    from django.contrib.auth.models import Group, Permission

    groups = models.ManyToManyField(Group, related_name="home_usuario_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="home_usuario_permissions"
    )
    tipo_usuario = models.CharField(max_length=11, choices=TIPOS)
    telefono = models.CharField(max_length=15, blank=True)


# Modelo para Eventos (común para ambos tipos)
class Event(models.Model):
    title = models.CharField(max_length=255, default="Título por defecto")
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", default="default_image.jpg")
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    highlight = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @classmethod
    def get_random_featured(cls, count=6):
        return cls.objects.filter(featured=True).order_by("?")[:count]

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:event_detail", args=[str(self.id)])
