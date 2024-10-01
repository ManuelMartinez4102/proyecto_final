from .models import MetasCumplidas, VentasUnitarias, Usuario
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncHour
from django.db.models import DecimalField
from django.db.models.functions import Coalesce

def calcular_ventas_totales(start_date, end_date):
    """Calcular las ventas totales en el rango de fechas especificado."""
    ventas_totales = MetasCumplidas.objects.filter(fecha_final_meta__range=[start_date, end_date])
    return ventas_totales.aggregate(Sum('monto_meta'))['monto_meta__sum'] or 0

def calcular_numero_ventas(start_date, end_date):
    """Calcular el número de ventas unitarias en el rango de fechas especificado."""
    ventas = VentasUnitarias.objects.filter(fecha__range=[start_date, end_date])
    return ventas.aggregate(Count('id_unitaria'))['id_unitaria__count'] or 0

def calcular_ganancias(start_date, end_date):
    """Calcular las ganancias en el rango de fechas especificado."""

    # Filtrar las ventas dentro del rango de fechas proporcionado
    ventas = VentasUnitarias.objects.filter(fecha__range=[start_date, end_date])

    # Anotar la ganancia por cada venta, calculada como (precio_publico - costo) * unidades_vendidas
    ventas = ventas.annotate(
        ganancia=ExpressionWrapper(
            (F('id_producto__precio_publico') - F('id_producto__costo')) * F('unidades_vendidas'),
            output_field=DecimalField()
        )
    )

    # Sumar las ganancias de todas las ventas en el rango de fechas
    total_ganancias = ventas.aggregate(total=Sum('ganancia'))['total'] or 0

    return total_ganancias

def calcular_porcentaje_metas_cumplidas(start_date, end_date):
    """Calcular el porcentaje de metas cumplidas en el rango de fechas especificado."""
    # Filtrar las metas cumplidas en el rango de fechas
    metas = MetasCumplidas.objects.filter(fecha_final_meta__range=[start_date, end_date])

    # Contar el total de metas y las metas cumplidas
    total_metas = metas.count()
    metas_cumplidas = metas.filter(meta_cumplida=True).count()

    # Calcular el porcentaje de metas cumplidas
    porcentaje_metas_cumplidas = (metas_cumplidas / total_metas * 100) if total_metas > 0 else 0

    return total_metas, metas_cumplidas, porcentaje_metas_cumplidas

def calcular_top_ventas(start_date, end_date):
    """Calcular el top de ventas basado en el precio público de los productos vendidos por usuarios con id_rol=2."""
    # Filtrar ventas por fecha y obtener solo los usuarios con `id_rol=2`
    ventas = VentasUnitarias.objects.filter(
        fecha__range=[start_date, end_date],
        id_usuario__id_rol=2  # Filtrar solo ventas realizadas por usuarios con id_rol=2
    )

    # Anotar la suma del precio público por cada venta y agrupar por nombre del usuario
    ventas = ventas.values('id_usuario__nombre').annotate(
        total_ventas=Sum(F('unidades_vendidas') * F('id_producto__precio_publico'))
    ).order_by('-total_ventas')  # Ordenar por ventas totales descendente

    # Crear listas de nombres y montos para la gráfica
    nombres_agentes = [venta['id_usuario__nombre'] for venta in ventas]
    montos_ventas = [venta['total_ventas'] for venta in ventas]

    return nombres_agentes, montos_ventas

def calcular_ventas_por_hora(start_date, end_date):
    """
    Calcular la cantidad de ventas realizadas por cada hora del día en el rango de fechas especificado,
    agrupando las ventas por horas truncadas (sin minutos ni segundos).
    """
    # Agrupar por hora truncada (solo la hora sin minutos ni segundos)
    ventas_horas = VentasUnitarias.objects.filter(
        fecha__range=[start_date, end_date]
    ).annotate(hora_truncada=TruncHour('hora'))  # Truncar la hora para quitar minutos y segundos
    # Agrupar por la hora truncada y contar las ventas en esa hora
    ventas_horas = ventas_horas.values('hora_truncada').annotate(ventas_por_hora=Count('id_unitaria')).order_by('hora_truncada')

    # Crear listas para la gráfica
    horas = [venta['hora_truncada'].strftime('%H:00') for venta in ventas_horas]  # Formatear horas a HH:00
    ventas = [venta['ventas_por_hora'] for venta in ventas_horas]

    return horas, ventas

def calcular_total_ventas_agente(start_date, end_date):
    """
    Calcular el número total de ventas (transacciones) por cada agente con id_rol=2 en el rango de fechas especificado.
    """
    # Filtrar las ventas en el rango de fechas y los usuarios con `id_rol=2`
    ventas = VentasUnitarias.objects.filter(
        fecha__range=[start_date, end_date],
        id_usuario__id_rol=2
    ).values('id_usuario__nombre').annotate(
        total_ventas=Count('id_unitaria')  # Contar cada venta realizada por el agente
    ).order_by('-total_ventas')  # Ordenar por el número total de ventas de forma descendente

    # Crear listas de nombres de agentes y sus ventas para la gráfica
    nombres_agentes = [venta['id_usuario__nombre'] for venta in ventas]
    cantidad_ventas = [venta['total_ventas'] for venta in ventas]

    return nombres_agentes, cantidad_ventas

def calcular_top_categorias(start_date, end_date):
    """
    Calcular el top de categorías basado en el número de productos vendidos.
    """
    # Filtrar ventas en el rango de fechas especificado
    ventas_categorias = VentasUnitarias.objects.filter(
        fecha__range=[start_date, end_date]
    ).values('id_producto__id_categoria__nombre').annotate(
        total_vendidos=Sum('unidades_vendidas')
    ).order_by('-total_vendidos')  # Ordenar de mayor a menor

    # Crear listas de nombres de categorías y el total de productos vendidos
    nombres_categorias = [venta['id_producto__id_categoria__nombre'] for venta in ventas_categorias]
    cantidades_vendidas = [venta['total_vendidos'] for venta in ventas_categorias]

    return nombres_categorias, cantidades_vendidas

def calcular_resumen_ventas(start_date, end_date):
    """
    Calcular el resumen de ventas con la información detallada de cada transacción.
    """
    resumen = VentasUnitarias.objects.filter(
        fecha__range=[start_date, end_date]
    ).select_related('id_usuario', 'id_producto').values(
        'id_usuario__id_usuario',  # Clave del usuario
        'id_usuario__nombre',  # Nombre del usuario
        'id_producto__nombre',  # Nombre del producto
        'unidades_vendidas',  # Cantidad vendida
        'id_producto__costo',  # Costo del producto
        'id_producto__precio_publico'  # Precio público
    ).order_by('id_usuario__nombre')  # Ordenar por nombre del usuario

    return resumen