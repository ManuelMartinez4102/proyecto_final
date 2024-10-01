from django.urls import path
from .views import DashboardView, FormularioView

app_name = 'modulo_agente'  # Asegúrate de que el nombre esté correcto

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),  # Ruta de Dashboard
    path('formulario/', FormularioView.as_view(), name='formulario'),  # Ruta de Formulario
]
