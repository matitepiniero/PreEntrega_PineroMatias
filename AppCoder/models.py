from django.db import models
import uuid
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# Create your models here.

class Cliente(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    cel=models.CharField(max_length=12)
    email=models.EmailField()

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barras = models.CharField(max_length=50, default=uuid.uuid4().hex)

    
    def __str__(self):
        return self.nombre

class TipoMovimiento(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Deposito(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    productos = models.ManyToManyField(Producto, through='StockDeposito')

    def __str__(self):
        return self.nombre
    
class StockDeposito(models.Model):
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.producto.nombre} en {self.deposito.nombre}'
    
class MovimientoStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('Ingreso', 'Ingreso'), ('Egreso', 'Egreso')])
    fecha = models.DateTimeField(auto_now_add=True)
    deposito = models.ForeignKey(Deposito, on_delete=models.CASCADE)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, on_delete=models.CASCADE)  # Cambia el campo a ForeignKey


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='', null=True, blank=True)


    def __str__(self):
        return self.user.username

