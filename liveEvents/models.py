from django.db import models
from home.models import Event


# Create your models here.

class LiveEvent(Event):
    event_ptr = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
    )
    location = models.CharField(max_length=200)
