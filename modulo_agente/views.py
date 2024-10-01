from django.shortcuts import render
from datetime import datetime
from django.views.generic import TemplateView


# Define DashboardView como clase basada en plantilla
class DashboardView(TemplateView):
    template_name = 'modulo_agente/dashboard.html'


# FormularioView - Si no existe, agrega una vista genérica
class FormularioView(TemplateView):
    template_name = 'modulo_agente/formulario.html'


# Función para analizar la fecha
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y')
    except (ValueError, TypeError):
        return None

# Vista para el dashboard del Agente
def agente_dashboard(request):
    # Obtener las fechas de los parámetros de la URL
    start_date = parse_date(request.GET.get('start_date'))
    end_date = parse_date(request.GET.get('end_date'))

    # Si no se seleccionaron fechas, usar el rango del mes actual
    if not start_date or not end_date:
        start_date = datetime.today().replace(day=1)  # Primer día del mes actual
        end_date = datetime.today()  # Fecha actual

    # Pasar las fechas seleccionadas al contexto
    context = {
        'start_date': start_date.strftime('%d/%m/%Y'),
        'end_date': end_date.strftime('%d/%m/%Y'),
    }

    return render(request, 'modulo_agente/dashboard.html', context)