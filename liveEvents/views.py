from datetime import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from liveEvents.models import LiveEvent

# Create your views here.


def create_live_event(request):
    if request.method == "POST":
        try:
            # Procesar los datos del formulario
            title = request.POST.get("title")
            description = request.POST.get("description")
            date_str = request.POST.get("date")
            time_str = request.POST.get("time")
            location = request.POST.get("location")
            image = request.FILES.get("image")

            # Validación básica
            if not all([title, description, date_str, time_str, location]):
                messages.error(
                    request, "Por favor complete todos los campos requeridos"
                )
                return render(request, "liveEvents/create_live_event.html")

            # Combinar fecha y hora y convertir a datetime
            datetime_str = f"{date_str} {time_str}"
            date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

            # Crear el evento
            event = LiveEvent(
                title=title,
                description=description,
                date=date,
                location=location,
                image=image,
            )

            if request.user.is_authenticated:
                event.created_by = request.user

            event.save()

            messages.success(request, "¡Evento Presencial creado exitosamente!")
            return redirect("home")

        except Exception as e:
            messages.error(request, f"Error al crear el evento: {str(e)}")
            return render(
                request, "create_live_event.html"
            )  # Renderiza de nuevo con error
    return render(request, 'create_live_event.html')
