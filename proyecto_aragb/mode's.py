# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# modulo_gerente/models.py

from django.db import models
from django.contrib.auth.hashers import make_password  # Importa la función para hashear contraseñas

class Usuario(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Ajusta la longitud si es necesario
    # Otros campos...

    def save(self, *args, **kwargs):
        # Hashea la contraseña antes de guardar
        if self.pk is None:  # Solo hashear si es un nuevo usuario
            self.password = make_password(self.password)
        else:
            # Si la contraseña no ha cambiado, no la vuelve a hashear
            if isinstance(self.password, str):
                self.password = make_password(self.password)
        super().save(*args, **kwargs)