from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home, name="home"),
    # path("login/", views.login_view, name="login"),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path(
        "login/",
        LoginView.as_view(
            template_name="login.html",
            redirect_authenticated_user=True,
            extra_context={"next": "/profile/"},
        ),
        name="login",
    ),
    path("registerUser/", views.register_User, name="registerUser"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("create-event/", views.create_event, name="create_event"),
    path("check-user/", views.check_user_status, name="check_user"),
    path("profile/", views.profile, name="profile"),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('events', views.eventListView.as_view(), name='event_list'),
    path('create/', views.eventCreateView.as_view(), name='event_virtual_create'),
]
