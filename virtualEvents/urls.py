from django.urls import path
from . import views

app_name = 'virtualEvents'

urlpatterns = [
    path('create/', views.create_virtual_event, name='create_virtual_event'),
    # ... otras URLs para eventos virtuales ...
]
