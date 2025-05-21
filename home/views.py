from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Event, User
from django.views.decorators.csrf import csrf_exempt

# Usar @csrf_exempt temporalmente (en producción quitarlo y usar {% csrf_token %} en los templates).


# Página principal con carrusel
def home(request):
    eventos_destacados = Event.objects.filter(destacado=True)[:6]  # 6 eventos para el carrusel
    return render(request, 'home.html', {'eventos': eventos_destacados})


# Todos los eventos (página aparte)
def all_events(request):
    eventos = Event.objects.all()
    return render(request, 'eventos.html', {'eventos': eventos})


# Procesar login (sin forms.py)
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


# Procesar registro (sin forms.py)
@csrf_exempt
def register_User(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password'],
            tipo_usuario=request.POST['tipo_usuario']
        )
        login(request, user)
        return redirect('home')
    return render(request, 'registerUser.html')


# Procesar creación de eventos (modal)
@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        evento = Event(
            creador=request.user,
            titulo=request.POST['titulo'],
            descripcion=request.POST['descripcion'],
            tipo=request.POST['tipo'],
            fecha=request.POST['fecha'],
            imagen=request.FILES['imagen']
        )
        if request.POST['tipo'] == 'VIRTUAL':
            evento.enlace_virtual = request.POST['enlace_virtual']
        else:
            evento.direccion = request.POST['direccion']
            evento.ciudad = request.POST['ciudad']
        evento.save()
        return redirect('home')
