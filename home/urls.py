from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_User, name='register'),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('create-event/', views.create_event, name='create_event'),
    path('events/', views.all_events, name='events'),
]
