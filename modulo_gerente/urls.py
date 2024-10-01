from django.urls import path
from .views import DashboardView, MetasView, DescansosView, DatosAgentesView, gerente_dashboard

app_name = 'modulo_gerente'

urlpatterns = [
    path('', gerente_dashboard, name='dashboard'),  # Enlazar correctamente con la vista del dashboard
    path('metas/', MetasView.as_view(), name='metas'),
    path('descansos/', DescansosView.as_view(), name='descansos'),
    path('datos_agentes/', DatosAgentesView.as_view(), name='datos_agentes'),
]