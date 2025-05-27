from django.urls import path
from . import views

app_name = 'liveEvents'

urlpatterns = [
    path('create/', views.create_live_event, name='create_live_event'),
]
