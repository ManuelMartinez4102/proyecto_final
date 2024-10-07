from django.db import models

# Create your models here.

# modulo_gerente/models.py
from django.db import models

# Modelo de la tabla 'rol'
class Rol(models.Model):
    id_rol = models.IntegerField(primary_key=True)
    puestos = models.CharField(max_length=255)
    roles = models.CharField(max_length=255)
    permisos = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.roles} - {self.puestos}"

    class Meta:
        db_table = 'rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


# Modelo de la tabla 'usuarios'
class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    clave = models.CharField(max_length=50)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='id_rol')  # Añadir `db_column='id_rol'`
    email = models.EmailField(max_length=255)
    sucursal = models.CharField(max_length=255)
    antiguedad = models.DateField()
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


# Modelo de la tabla 'metas_diarias'
class MetasDiarias(models.Model):
    id_meta = models.IntegerField(primary_key=True)
    meta_ventas = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()

    def __str__(self):
        return f"Meta {self.id_meta} - Ventas: {self.meta_ventas}"

    class Meta:
        db_table = 'metas_diarias'
        verbose_name = 'Meta Diaria'
        verbose_name_plural = 'Metas Diarias'


# Modelo de la tabla 'categorias'
class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'


# Modelo de la tabla 'productos'
class Producto(models.Model):
    id_producto = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')  # Agregar db_column aquí
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_publico = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


# Modelo de la tabla 'ventas_unitarias' (modulo_gerente/models.py)
class VentasUnitarias(models.Model):
    id_unitaria = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    fecha = models.DateField()
    hora = models.TimeField()
    unidades_vendidas = models.IntegerField(default=1)

    def __str__(self):
        return f"Venta {self.id_unitaria} - Usuario: {self.id_usuario}"

    class Meta:
        db_table = 'ventas_unitarias'

# Modelo de la tabla 'ventas_totales'
class VentasTotales(models.Model):
    id_venta_total = models.IntegerField(primary_key=True)
    id_meta = models.ForeignKey(MetasDiarias, on_delete=models.CASCADE)
    id_unitaria = models.ForeignKey(VentasUnitarias, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    meta_cumplida = models.BooleanField()

    def __str__(self):
        return f"Venta Total {self.id_venta_total} - Monto: {self.monto_total}"

    class Meta:
        db_table = 'ventas_totales'
        verbose_name = 'Venta Total'
        verbose_name_plural = 'Ventas Totales'


from django.db import models

class MetasCumplidas(models.Model):
    id_total = models.AutoField(primary_key=True)
    id_meta = models.IntegerField()
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')  # Relación con Usuario
    monto_meta = models.DecimalField(max_digits=10, decimal_places=2)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_final_meta = models.DateField()
    meta_cumplida = models.BooleanField()

    def __str__(self):
        return f"Meta {self.id_meta} - Cumplida: {self.meta_cumplida}"

    class Meta:
        db_table = 'metas_cumplidas'
