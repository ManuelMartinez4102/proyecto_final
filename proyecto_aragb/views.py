# proyecto_aragb/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from modulo_gerente.models import Usuario  # Asegúrate de que `Usuario` esté importado correctamente


# Vista para el Dashboard principal
def home_view(request):
    return render(request, 'home/home.html')  # Ruta a la plantilla del home


# Vista para el inicio de sesión

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from modulo_gerente.models import Usuario


def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('txtEmail')
        contrasena = request.POST.get('txtPassword')

        try:
            usuario = Usuario.objects.get(email=correo)
            if check_password(contrasena, usuario.password):  # Verifica la contraseña hasheada
                # Establece la sesión con los atributos correctos
                request.session['logueado'] = True
                request.session['id_usuario'] = usuario.id_usuario  # Cambia aquí

                # Cambia esto para acceder al campo correcto
                request.session['id_rol'] = usuario.id_rol.id_rol  # Cambia 'id' a 'id_rol'

                # Redirigir según el rol del usuario
                if request.session['id_rol'] == 1:
                    return redirect('modulo_gerente:dashboard')  # Asegúrate de que esta ruta está definida
                elif request.session['id_rol'] == 2:
                    return redirect('modulo_agente:dashboard')
                else:
                    messages.error(request, "Rol de usuario no reconocido.")

            else:
                messages.error(request, "Contraseña incorrecta.")
        except Usuario.DoesNotExist:
            messages.error(request, "No se encontró un usuario con ese correo.")

    return render(request, 'home/login.html')

