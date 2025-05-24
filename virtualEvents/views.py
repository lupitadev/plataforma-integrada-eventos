from django.shortcuts import render

# Create your views here.


def create_event(request):
    # Tu lógica para eventos presenciales
    return render(request, 'create_virtual_event.html')
