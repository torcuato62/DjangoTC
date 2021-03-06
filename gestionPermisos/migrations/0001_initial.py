# Generated by Django 3.1.1 on 2020-10-02 21:09

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
            name='Estado',
            fields=[
                ('estId', models.AutoField(primary_key=True, serialize=False)),
                ('estDescripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('secCodigo', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='Codigo')),
                ('secSector', models.CharField(max_length=40, verbose_name='Sector')),
            ],
        ),
        migrations.CreateModel(
            name='TipoPermiso',
            fields=[
                ('tperId', models.AutoField(primary_key=True, serialize=False)),
                ('tperDescripcion', models.CharField(max_length=50)),
                ('tperCtaCte', models.BooleanField(blank=True, null=True)),
                ('tperActivo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('perIdpermiso', models.AutoField(primary_key=True, serialize=False)),
                ('perFechaHora', models.DateTimeField(auto_now=True)),
                ('perMotivo', models.TextField(blank=True, null=True)),
                ('perFechaDesde', models.DateField(blank=True, null=True)),
                ('perFechaHasta', models.DateField(blank=True, null=True)),
                ('perEstado', models.IntegerField(default=1)),
                ('perHoraIngreso', models.TimeField(blank=True, null=True)),
                ('perHoraRetiro', models.TimeField(blank=True, null=True)),
                ('perCantidadDias', models.IntegerField(blank=True, null=True)),
                ('perCertificado', models.BooleanField(blank=True, null=True)),
                ('perCertificadoVisita', models.BooleanField(blank=True, null=True)),
                ('perMotivor', models.IntegerField(blank=True, null=True)),
                ('perDescuento96', models.BooleanField(blank=True, null=True)),
                ('perArticuloE', models.BooleanField(blank=True, null=True)),
                ('perFechaVisado', models.DateTimeField(blank=True, null=True)),
                ('perIPVisado', models.GenericIPAddressField(blank=True, null=True)),
                ('perFechaAutorizado', models.DateTimeField(blank=True, null=True)),
                ('perIPAutorizado', models.GenericIPAddressField(blank=True, null=True)),
                ('perFechaAceptado', models.DateTimeField(blank=True, null=True)),
                ('perIPAceptado', models.GenericIPAddressField(blank=True, null=True)),
                ('perVisadoSolicitante', models.IntegerField(blank=True, null=True)),
                ('perAnioLicencia', models.IntegerField(blank=True, null=True)),
                ('perDiasdeViaje', models.IntegerField(blank=True, null=True)),
                ('perProcesadoRRHH', models.DateTimeField(blank=True, null=True)),
                ('perCodigoCargado', models.DateTimeField(blank=True, null=True)),
                ('perFechaFinSolicitud', models.DateTimeField(blank=True, null=True)),
                ('perDetalleCargado', models.DateTimeField(blank=True, null=True)),
                ('perTPermiso', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='gestionPermisos.tipopermiso')),
                ('perUsuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='perUsr', to=settings.AUTH_USER_MODEL)),
                ('perUsuarioAcepta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='perUsrAcepta', to=settings.AUTH_USER_MODEL)),
                ('perUsuarioAutoriza', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='perUsrAutoriza', to=settings.AUTH_USER_MODEL)),
                ('perUsuarioVisa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='perUsrVisa', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('legCodigo', models.IntegerField(primary_key=True, serialize=False, verbose_name='Código')),
                ('legLegajo', models.CharField(max_length=15)),
                ('legNombre', models.CharField(max_length=40)),
                ('legActivo', models.BooleanField(default=True, null=True)),
                ('legFechaEgreso', models.DateField(blank=True, null=True, verbose_name='Fecha Egreso')),
                ('legTarjeta', models.CharField(blank=True, max_length=8, null=True, verbose_name='Tarjeta')),
                ('legCUIL', models.CharField(blank=True, max_length=18, null=True, verbose_name='CUIL')),
                ('legTelefono', models.CharField(blank=True, max_length=18, null=True, verbose_name='Teléfono')),
                ('legTipodeDocumento', models.IntegerField(blank=True, null=True, verbose_name='Tipo Documento')),
                ('legDocumento', models.CharField(blank=True, max_length=20, null=True, verbose_name='Documento')),
                ('legSuspendido', models.BooleanField(null=True)),
                ('legFechadeNacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha Nacimiento')),
                ('legGenero', models.IntegerField(blank=True, null=True, verbose_name='Género')),
                ('legEmailPersonal', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Personal')),
                ('legEmailLaboral', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Laboral')),
                ('legSector', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='gestionPermisos.sector')),
            ],
        ),
    ]
