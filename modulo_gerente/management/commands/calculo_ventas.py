# modulo_gerente/management/commands/actualizar_metas.py
from django.core.management.base import BaseCommand
from django.db.models import Sum, F
from modulo_gerente.models import MetasDiarias, Usuario, VentasUnitarias, MetasCumplidas

class Command(BaseCommand):
    help = 'Calcula el cumplimiento de todas las metas existentes y actualiza la tabla metas_cumplidas.'

    def handle(self, *args, **options):
        # Obtener todas las metas activas
        metas = MetasDiarias.objects.all()
        self.stdout.write(f"Calculando cumplimiento de {metas.count()} metas...")

        # Iterar por cada meta
        for meta in metas:
            fecha_inicio = meta.fecha_inicio
            fecha_final = meta.fecha_final

            # Filtrar las ventas unitarias dentro del rango de la meta actual
            ventas_unitarias = VentasUnitarias.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_final)

            # Si no hay ventas en el rango de la meta, marcar la meta como no cumplida con monto 0
            if not ventas_unitarias.exists():
                MetasCumplidas.objects.update_or_create(
                    id_meta=meta.id_meta,  # Usar `meta.id_meta`
                    id_usuario=None,
                    defaults={
                        'monto_meta': meta.meta_ventas,
                        'monto_total': 0,
                        'fecha_final_meta': meta.fecha_final,
                        'meta_cumplida': 0  # No cumplida
                    }
                )
                self.stdout.write(f"Meta {meta.id_meta} - No se encontraron ventas. Meta no cumplida.")
                continue

            # Agrupar ventas por usuario y calcular el monto total para cada usuario
            ventas_por_usuario = ventas_unitarias.values('id_usuario').annotate(
                monto_total=Sum(F('unidades_vendidas') * F('id_producto__precio_publico'))
            )

            # Crear o actualizar resultados de ventas totales para cada usuario y meta
            for venta in ventas_por_usuario:
                id_usuario = venta['id_usuario']
                monto_total = venta['monto_total'] or 0
                meta_cumplida = monto_total >= meta.meta_ventas

                # Actualizar usando solo el id del usuario y no el objeto Usuario completo
                MetasCumplidas.objects.update_or_create(
                    id_meta=meta.id_meta,  # Usar `meta.id_meta`
                    id_usuario=id_usuario,  # Aquí cambiamos el objeto Usuario por su ID
                    defaults={
                        'monto_meta': meta.meta_ventas,
                        'monto_total': monto_total,
                        'fecha_final_meta': meta.fecha_final,
                        'meta_cumplida': 1 if meta_cumplida else 0
                    }
                )

            self.stdout.write(f"Meta {meta.id_meta} - Resultados calculados y guardados en la base de datos.")

        self.stdout.write("Proceso de cálculo y actualización de metas completado.")
