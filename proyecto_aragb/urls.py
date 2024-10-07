"""
URL configuration for proyecto_aragb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


# proyecto_aragb/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import home_view, login_view  # Importa las vistas `home_view` y `login_view` desde views.py

urlpatterns = [
    path('', home_view, name='home'),  # Página de inicio
    path('login/', login_view, name='login'),  # Página de inicio de sesión
    path("admin/", admin.site.urls),
    path('gerente/', include('modulo_gerente.urls')),  # Módulo para la vista del gerente
    path('agente/', include('modulo_agente.urls')),  # Módulo para la vista del agente
]