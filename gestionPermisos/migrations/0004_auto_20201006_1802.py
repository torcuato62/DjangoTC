# Generated by Django 3.1.1 on 2020-10-06 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPermisos', '0003_auto_20201006_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permiso',
            name='perVisadoSolicitante',
        ),
        migrations.AddField(
            model_name='permiso',
            name='perVistoSolicitante',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]