# Generated by Django 3.1.7 on 2021-03-07 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='tipo_pago',
        ),
        migrations.AddField(
            model_name='turno',
            name='fecha',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='turno',
            name='horario',
            field=models.TimeField(default=None),
        ),
        migrations.AddField(
            model_name='turno',
            name='vehiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.vehiculo'),
        ),
    ]