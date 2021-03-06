# Generated by Django 3.1.1 on 2020-10-09 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestionPermisos', '0007_auto_20201009_1505'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sector',
            name='secResponsable',
        ),
        migrations.AddField(
            model_name='responsablesector',
            name='resSector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='resSec', to='gestionPermisos.sector', verbose_name='Sector a Cargo'),
        ),
        migrations.AddField(
            model_name='responsablesector',
            name='ressecId',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='responsablesector',
            name='resUsuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='resUsr', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Responsable'),
        ),
        migrations.AddConstraint(
            model_name='responsablesector',
            constraint=models.UniqueConstraint(fields=('resUsuario', 'resSector'), name='UsrSecUnica'),
        ),
    ]
