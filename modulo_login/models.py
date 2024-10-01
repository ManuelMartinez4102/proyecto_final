# En modulo_login/models.py

from django.db import models

class Usuario(models.Model):
    # Asegúrate de que estos campos estén correctamente indentados
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)

    class Meta:
        db_table = 'usuario_login'  # Nombre de tabla único
