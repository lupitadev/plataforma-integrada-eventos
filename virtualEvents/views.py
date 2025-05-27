import datetime
from django.shortcuts import render, redirect
from .models import VirtualEvent
from django.contrib import messages

# Create your views here.


def create_virtual_event(request):
    if request.method == "POST":
        try:
            # Procesar los datos del formulario
            title = request.POST.get("title")
            description = request.POST.get("description")
            date_str = request.POST.get("date")
            time_str = request.POST.get("time")
            link = request.POST.get("link")
            image = request.FILES.get("image")

            # Validación básica
            if not all([title, description, date_str, time_str, link]):
                messages.error(
                    request, "Por favor complete todos los campos requeridos"
                )
                return render(request, "virtualEvents/create_virtual_event.html")

            # Combinar fecha y hora
            datetime_str = f"{date_str} {time_str}"
            date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

            # Crear el evento
            event = VirtualEvent(
                title=title,
                description=description,
                date=date,
                link=link,
                image=image,
            )

            if request.user.is_authenticated:
                event.created_by = request.user

            event.save()

            messages.success(request, "¡Evento virtual creado exitosamente!")
            return redirect(
                "virtual_events:list"
            )  # Asegúrate de tener esta URL definida

        except Exception as e:
            messages.error(request, f"Error al crear el evento: {str(e)}")

    return render(request, "create_virtual_event.html")
