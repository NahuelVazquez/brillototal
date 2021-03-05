# Generated by Django 3.1.7 on 2021-02-25 02:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.IntegerField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lavado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_lavado', models.CharField(choices=[('interior', 'Interior'), ('exterior', 'Exterior'), ('completo', 'Completo')], max_length=8)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_vehiculo', models.CharField(choices=[('auto', 'Auto'), ('camioneta', 'Camioneta'), ('moto', 'Moto')], max_length=9)),
                ('matricula', models.CharField(max_length=20)),
                ('marca', models.CharField(max_length=20)),
                ('modelo', models.CharField(max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pago', models.CharField(choices=[('efectivo', 'Efectivo'), ('credito', 'Tarjeta crédito'), ('debito', 'Tarjeta débito')], max_length=8)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.cliente')),
                ('lavado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.lavado')),
            ],
        ),
    ]