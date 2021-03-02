from django.db import models
from django.contrib.auth.models import User


TIPO_LAVADO = (
       ('interior', 'Interior' ),
       ('exterior', 'Exterior' ),
       ('completo', 'Completo'),
   )

TIPO_VEHICULO = (
       ('auto', 'Auto' ),
       ('camioneta', 'Camioneta' ),
       ('moto', 'Moto'),
   )
TIPO_PAGO = (
       ('efectivo', 'Efectivo' ),
       ('credito', 'Tarjeta crédito' ),
       ('debito', 'Tarjeta débito' ),
   )


class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    telefono = models.IntegerField()

    def __str__(self):
        return self.usuario.username


class Lavado(models.Model):
    tipo_lavado = models.CharField(max_length=8, choices=TIPO_LAVADO)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


class Vehiculo(models.Model):
    tipo_vehiculo = models.CharField(max_length=9, choices=TIPO_VEHICULO)
    matricula = models.CharField(max_length=20)
    marca = models.CharField (max_length=20)
    modelo = models.CharField(max_length=20)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)


class Turno(models.Model):
    fecha = models.DateTimeField
    tipo_pago = models.CharField(max_length=8, choices=TIPO_PAGO)
    lavado = models.ForeignKey(Lavado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
