# Generated by Django 3.1.1 on 2020-11-11 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201103_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='maxAceptaPermisos',
            field=models.IntegerField(default=5),
        ),
    ]
