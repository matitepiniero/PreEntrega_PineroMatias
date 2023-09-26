from django.db import models

# Create your models here.

class Cliente(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    cel=models.CharField(max_length=12)
    email=models.EmailField()

class Profesor(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    email=models.EmailField()
    profesion= models.CharField(max_length=30)

class Curso(models.Model):
    nombre= models.CharField(max_length=30)
    comision =models.IntegerField()

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)  # Agrega un campo único para el código
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)  # Utiliza DecimalField para manejar los precios

    def __str__(self):
        return self.nombre
