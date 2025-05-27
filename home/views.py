import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from liveEvents.models import LiveEvent
from virtualEvents.models import VirtualEvent
from .models import Event
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

# Usar @csrf_exempt temporalmente (en producción quitarlo y usar {% csrf_token %} en los templates).


# Página principal con carrusel
def home(request):
    from itertools import chain

    live = LiveEvent.objects.filter(is_active=True)[:3]
    virtual = VirtualEvent.objects.filter(is_active=True)[:3]
    random_events = list(chain(live, virtual))
    random.shuffle(random_events)

    return render(request, "home.html", {"random_events": random_events})


# Todos los eventos (página aparte)
def all_events(request):
    eventos = Event.objects.all()
    return render(request, "eventos.html", {"eventos": eventos})


# Procesar login (sin forms.py)
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
    return render(request, "login.html")


# Procesa logout
@require_POST  # Asegura que solo se pueda acceder por POST
def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect("home")


# Procesar registro (sin forms.py)
@csrf_protect
def register_User(request):
    # Si el usuario ya está autenticado, redirigir al perfil
    if request.user.is_authenticated:
        return redirect("profile")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Autenticación automática con verificación
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "¡Registro exitoso! Bienvenido/a.")
                return redirect("profile")
            else:
                messages.error(request, "Error en la autenticación automática.")
        else:
            # Mostrar todos los errores de validación
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()

    return render(request, "registerUser.html", {"form": form})


# Interfaz del perfil de usuario
@csrf_exempt
def profile(request):
    return render(request, "profile.html")


# Verifica si el usuario existe en la base de datos
@csrf_exempt
def check_user_status(request):
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True, "registered": True})

    # No necesita verificar si el usuario existe, solo si está autenticado
    return JsonResponse({"authenticated": False, "registered": False})


# Procesar creación de eventos (modal)
@csrf_exempt
def create_event(request):
    if request.method == "POST":
        evento = Event(
            creador=request.user,
            titulo=request.POST["titulo"],
            descripcion=request.POST["descripcion"],
            tipo=request.POST["tipo"],
            fecha=request.POST["fecha"],
            imagen=request.FILES["imagen"],
        )
        if request.POST["tipo"] == "VIRTUAL":
            evento.enlace_virtual = request.POST["enlace_virtual"]
        else:
            evento.direccion = request.POST["direccion"]
            evento.ciudad = request.POST["ciudad"]
        evento.save()
        return redirect("home")


class eventListView(ListView):
    model = VirtualEvent
    template_name = "event_list.html"
    context_object_name = "events"
    ordering = ["-date"]  # Ordenar por fecha más reciente
    paginate_by = 10  # Opcional: paginación

    def get_queryset(self):
        # Filtra solo eventos activos y futuros/pasados según necesites
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Upcoming Events"
        return context


class eventCreateView(CreateView):
    model = Event
    template_name = "events/event_form.html"
    success_url = reverse_lazy("event_list")
    fields = [
        "title",
        "description",
        "date",
        "location",
        "image",
        "featured",
    ]  # Todos los campos que necesitas

    def form_valid(self, form):
        # Asigna el usuario actual como creador (opcional)
        if self.request.user.is_authenticated:
            form.instance.creator = self.request.user

        # Mensaje de éxito
        messages.success(self.request, "Evento creado exitosamente!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Mensaje de error
        messages.error(self.request, "Error al crear el evento. Verifica los datos.")
        return super().form_invalid(form)
