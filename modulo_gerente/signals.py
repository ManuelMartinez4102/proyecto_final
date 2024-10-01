
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MetasDiarias, Usuario, VentasUnitarias, MetasCumplidas
from django.db.models import Sum, F

@receiver(post_save, sender=MetasDiarias)
def calcular_metas_automaticamente(sender, instance, created, **kwargs):
    # Este bloque de código se ejecuta cada vez que se guarda o actualiza un registro en MetasDiarias
    meta = instance
    fecha_inicio = meta.fecha_inicio
    fecha_final = meta.fecha_final

    # Filtrar las ventas unitarias dentro del rango de la meta actual
    ventas_unitarias = VentasUnitarias.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_final)

    # Si no hay ventas en el rango de la meta, marcar la meta como no cumplida con monto 0
    if not ventas_unitarias.exists():
        MetasCumplidas.objects.update_or_create(
            id_meta=meta.id_meta,  # Cambiado a meta.id_meta en lugar de meta
            id_usuario=None,
            defaults={
                'monto_meta': meta.meta_ventas,
                'monto_total': 0,
                'fecha_final_meta': meta.fecha_final,
                'meta_cumplida': 0  # No cumplida
            }
        )
        return

    # Agrupar ventas por usuario y calcular el monto total para cada usuario
    ventas_por_usuario = ventas_unitarias.values('id_usuario').annotate(
        monto_total=Sum(F('unidades_vendidas') * F('id_producto__precio_publico'))
    )

    # Actualizar o crear resultados de ventas totales para cada usuario y meta
    for venta in ventas_por_usuario:
        id_usuario = venta['id_usuario']
        monto_total = venta['monto_total'] or 0
        meta_cumplida = monto_total >= meta.meta_ventas

        MetasCumplidas.objects.update_or_create(
            id_meta=meta.id_meta,  # Cambiado a meta.id_meta en lugar de meta
            id_usuario=Usuario.objects.get(id_usuario=id_usuario),
            defaults={
                'monto_meta': meta.meta_ventas,
                'monto_total': monto_total,
                'fecha_final_meta': meta.fecha_final,
                'meta_cumplida': 1 if meta_cumplida else 0
            }
        )