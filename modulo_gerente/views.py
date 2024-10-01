from django.shortcuts import render
from datetime import datetime
from django.views.generic import TemplateView
from .utils import calcular_ventas_totales, calcular_numero_ventas, calcular_ganancias, calcular_porcentaje_metas_cumplidas, calcular_top_ventas, calcular_ventas_por_hora
from .utils import calcular_total_ventas_agente, calcular_top_categorias, calcular_resumen_ventas

# Define DashboardView como clase basada en plantilla
class DashboardView(TemplateView):
    template_name = 'modulo_gerente/dashboard.html'

# MetasView - si no existe, agrega una vista genérica como esta
class MetasView(TemplateView):
    template_name = 'modulo_gerente/metas.html'

# DescansosView - si no existe, agrega una vista genérica
class DescansosView(TemplateView):
    template_name = 'modulo_gerente/descansos.html'

# DatosAgentesView - si no existe, agrega una vista genérica
class DatosAgentesView(TemplateView):
    template_name = 'modulo_gerente/datos_agentes.html'

# Función para analizar la fecha
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y')
    except (ValueError, TypeError):
        return None


# Vista del Dashboard del Gerente
def gerente_dashboard(request):
    # Obtener las fechas de los parámetros de la URL
    start_date = parse_date(request.GET.get('start_date'))
    end_date = parse_date(request.GET.get('end_date'))

    # Si no se seleccionaron fechas, usar el rango del mes actual
    if not start_date or not end_date:
        start_date = datetime.today().replace(day=1)  # Primer día del mes actual
        end_date = datetime.today()  # Fecha actual

    # Calcular los KPIs usando funciones auxiliares
    total_ventas = calcular_ventas_totales(start_date, end_date)
    numero_ventas = calcular_numero_ventas(start_date, end_date)
    ganancias = calcular_ganancias(start_date, end_date)

    # Calcular las metas cumplidas y el total de metas usando el rango de fechas seleccionado
    total_metas, metas_cumplidas, porcentaje_metas_cumplidas = calcular_porcentaje_metas_cumplidas(start_date, end_date)

    # Calcular el top de ventas por agente basado en las fechas seleccionadas
    nombres_agentes, montos_ventas = calcular_top_ventas(start_date, end_date)

    # Calcular la cantidad de ventas por hora del día
    horas, ventas_por_hora = calcular_ventas_por_hora(start_date, end_date)

    # Calcular las ventas totales por agente
    nombres_agentes_2, montos_ventas_2 = calcular_total_ventas_agente(start_date, end_date)

    # productos y resumen
    nombres_categorias, cantidades_vendidas = calcular_top_categorias(start_date, end_date)  # Categorías de productos
    resumen_ventas = calcular_resumen_ventas(start_date, end_date)  # Resumen de ventas detallado


    # Pasar las fechas seleccionadas y los KPIs al contexto
    context = {
        'total_ventas': total_ventas,
        'numero_ventas': numero_ventas,
        'ganancias': ganancias,
        'total_metas': total_metas,
        'metas_cumplidas': metas_cumplidas,
        'porcentaje_metas_cumplidas': porcentaje_metas_cumplidas,
        'nombres_agentes': nombres_agentes,  # Lista de nombres como ["Carlos", "Ana", "Juan"]
        'montos_ventas': [float(v) for v in montos_ventas],  # Convertir a flotantes
        'horas': horas,  # Agregar las horas para la gráfica de tendencias
        'ventas_por_hora': ventas_por_hora,  # Agregar el número de ventas por hora

        'nombres_agentes_2': nombres_agentes_2,  # Nombres de los agentes
        'montos_ventas_2': [float(v) for v in montos_ventas_2],  # Convertir a flotantes

        'nombres_categorias': nombres_categorias,
        'cantidades_vendidas': cantidades_vendidas,
        'resumen_ventas': resumen_ventas,  # Pasar el resumen de ventas a la plantilla

        'start_date': start_date.strftime('%d/%m/%Y'),
        'end_date': end_date.strftime('%d/%m/%Y'),
    }

    return render(request, 'modulo_gerente/dashboard.html', context)