# Generated by Django 3.1.7 on 2021-03-07 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210307_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='horario',
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha',
            field=models.DateTimeField(default=None),
        ),
    ]