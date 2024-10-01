from django.contrib import admin

# Register your models here.

# modulo_gerente/admin.py
from django.contrib import admin
from .models import Rol, Usuario, MetasDiarias, Categoria, Producto, VentasUnitarias, VentasTotales

admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(MetasDiarias)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(VentasUnitarias)
admin.site.register(VentasTotales)