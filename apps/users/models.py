from django.db import models
from django.contrib.auth.models import User


TIPO_LAVADO = (
    ('interior', 'Interior'),  # 400
    ('exterior', 'Exterior'),  # 300
    ('completo', 'Completo'),  # 600
)

TIPO_VEHICULO = (
    ('auto', 'Auto'),  # 1
    ('camioneta', 'Camioneta'),  # 1.25
    ('moto', 'Moto'),  # .75
)


class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    telefono = models.IntegerField()

    def __str__(self):
        return self.usuario.username


class Lavado(models.Model):
    tipo_lavado = models.CharField(max_length=8, choices=TIPO_LAVADO)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo_lavado} - ${self.precio}"

    @classmethod
    def get_lavados(cls):
        return [lavado[0] for lavado in TIPO_LAVADO]


class Vehiculo(models.Model):
    tipo_vehiculo = models.CharField(max_length=9, choices=TIPO_VEHICULO)
    matricula = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)


class Turno(models.Model):
    # AQUI DEBERIA ELEGIR EL USUARIO DIA Y HORA (Lun a sabado // 8 a 19 hs // 1 hora por turno.)
    fecha = models.DateTimeField(default=None)
    lavado = models.ForeignKey(Lavado, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
