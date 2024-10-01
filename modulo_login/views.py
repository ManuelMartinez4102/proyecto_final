from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario

# Vista para el Dashboard principal
def home_view(request):
    return render(request, 'home/home.html')  # Asegúrate de que esta plantilla existe

class Login(TemplateView):
    template_name = 'home/login.html'  # Puedes usar esta clase si lo prefieres, pero no es necesario aquí

def login_view(request):
    if request.method == 'POST':
        _email = request.POST.get('txtEmail')
        _password = request.POST.get('txtPassword')

        try:
            account = Usuario.objects.get(email=_email, password=_password)
            request.session['logueado'] = True
            request.session['id_usuario'] = account.id
            request.session['id_rol'] = account.id_rol

            # Redirigir según el rol del usuario
            if request.session['id_rol'] == 1:
                return redirect('modulo_gerente.urls')  # Asegúrate de que esta ruta está definida
            elif request.session['id_rol'] == 2:
                return redirect('modulo_agente.urls')  # Asegúrate de que esta ruta está definida
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o Contraseña Incorrectas")

    return render(request, 'home/login.html')  # Asegúrate de que esta plantilla existe
